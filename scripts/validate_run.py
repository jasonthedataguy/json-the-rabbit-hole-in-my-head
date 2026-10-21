#!/usr/bin/env python3
"""Zero-dependency local checks for .json chapter run manifests.

Usage: python scripts/validate_run.py path/to/run-manifest.json
This checks internal consistency, NOT external evidence or authorization.
"""
import json
import sys
from pathlib import Path

ALLOWED = {'not_started', 'in_progress', 'blocked', 'ready_for_review', 'approved', 'skipped'}
STAGES = [f'S{i:02d}_{label}' for i, label in enumerate([
    'intake', 'editorial_diagnosis', 'canonical', 'narration_script',
    'digital_reader', 'design', 'audio_film', 'campaign_assets',
    'product_strategy', 'commerce', 'release', 'learning'
])]

SURFACES = {'reader', 'film', 'social', 'audio', 'digital_product', 'physical_product'}


def required_public_flags(manifest):
    """Legacy records retain the full reader/film/social release contract."""
    scope = manifest.get('release_scope')
    surfaces = scope.get('surfaces', []) if isinstance(scope, dict) else ['reader', 'film', 'social']
    required = {'author_approved', 'founder_public_release_approved', 'privacy_rights_approved',
                'reader_verified_live', 'reader_live_url', 'website_cta_verified'}
    if 'film' in surfaces or 'audio' in surfaces:
        required.update({'script_facts_approved', 'narration_recorded_by_author'})
    if 'film' in surfaces or 'social' in surfaces:
        required.add('marketing_assets_qa_passed')
    return surfaces, required

def check(manifest):
    errors = []
    warnings = []
    stages = manifest.get('stages', {})
    if manifest.get('schema_version') != '1.0':
        warnings.append('Schema version differs from validated example 1.0.')
    for stage in STAGES:
        if stage not in stages:
            errors.append(f'Missing stage: {stage}')
        elif stages[stage] not in ALLOWED:
            errors.append(f'Invalid status for {stage}: {stages[stage]}')
        elif stages[stage] == 'skipped' and stage != 'S09_commerce' and not manifest.get('stage_evidence', {}).get(stage):
            warnings.append(f'Skipped stage {stage} should include a documented rationale.')
    if manifest.get('author_approved') and not (manifest.get('canonical_source_path') and manifest.get('canonical_sha256') and manifest.get('source_facts_approval_evidence')):
        errors.append('Author approval requires canonical path, SHA256 and approval evidence.')
    if stages.get('S02_canonical') == 'approved' and not manifest.get('author_approved'):
        errors.append('Canonical stage approved without explicit author_approved=true.')
    if stages.get('S03_narration_script') == 'approved' and not (manifest.get('author_approved') and manifest.get('script_facts_approved')):
        errors.append('Script cannot be approved without canonical and script-facts approval.')
    if stages.get('S06_audio_film') == 'approved' and not manifest.get('narration_recorded_by_author'):
        errors.append('Author-VO film cannot be approved without real author narration.')
    surfaces, required = required_public_flags(manifest)
    if not surfaces or any(surface not in SURFACES for surface in surfaces):
        errors.append('release_scope.surfaces must contain supported, explicitly selected surfaces.')
    public_ready = bool(surfaces) and all(bool(manifest.get(k)) for k in required) and manifest.get('public_visibility_policy') not in ('undecided', None, '')
    if any(s in surfaces for s in ('digital_product', 'physical_product')):
        public_ready = public_ready and all(bool(manifest.get(k)) for k in ('selected_revenue_offer', 'commerce_checkout_and_fulfillment_tested', 'founder_paid_release_approved'))
    if stages.get('S10_release') == 'approved' and not public_ready:
        errors.append('Public release approved without all required source/privacy/live-reader/CTA/media/founder gates.')
    if manifest.get('founder_paid_release_approved') or stages.get('S09_commerce') == 'approved':
        if not manifest.get('commerce_checkout_and_fulfillment_tested') or not manifest.get('selected_revenue_offer'):
            errors.append('Paid readiness requires selected offer and checkout/fulfillment tests.')
        if not (manifest.get('author_approved') and manifest.get('privacy_rights_approved')):
            errors.append('Paid readiness requires content and rights approval.')
    if stages.get('S11_learning') == 'approved' and not manifest.get('observed_metrics'):
        warnings.append('Learning approved with no observed metrics; document justified noninstrumentation.')
    for artifact in manifest.get('derivatives', []):
        if isinstance(artifact, dict) and artifact.get('status') == 'approved' and not artifact.get('evidence'):
            warnings.append(f'Approved artifact {artifact.get("id", "unnamed")} has no evidence link.')
    return errors, warnings, public_ready

def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as exc:
        print(f'ERROR reading manifest: {exc}')
        return 2
    errors, warnings, ready = check(data)
    print(f'Story: {data.get("story_id", "unknown")}  |  Public-ready consistency: {"YES" if ready else "NO"}')
    for item in errors: print('ERROR:', item)
    for item in warnings: print('WARN:', item)
    print(f'Validation: {len(errors)} error(s), {len(warnings)} warning(s).')
    return 1 if errors else 0

if __name__ == '__main__':
    sys.exit(main())
