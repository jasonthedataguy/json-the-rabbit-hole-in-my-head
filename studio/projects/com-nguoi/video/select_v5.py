"""Select the verified v5 review; retain all author/public/paid decisions."""
import argparse
from pathlib import Path
import copy
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'scripts'))
from studio import load, save, sha, validate_timeline


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--editor-visual-reviewed',action='store_true')
    args=parser.parse_args()
    if not args.editor_visual_reviewed:
        raise ValueError('Inspect the opening, both GIFs, controls and all reading-cue contact sheets first.')
    project_path=ROOT/'studio/projects/com-nguoi/project.json'
    project=load(project_path)
    base=project_path.parent
    qa=base/'video/review/v5-living-illustrations'
    report_path=qa/'verification.json'
    report=load(report_path)
    motion_path=qa/'motion-controls/verification.json'
    motion=load(motion_path)
    manifest_path=base/'animation/v5/motion-manifest.json'
    manifest=load(manifest_path)
    timeline_path=base/'video/timeline-v5.json'
    timeline=load(timeline_path)
    video=Path(manifest['outputPath'])
    assert report['technical_status']=='pass' and motion['status']=='pass'
    assert report['video_sha256']==sha(video)
    assert (report['duration_s'],report['frames_decoded'],report['audio_tracks'])==(120.0,3600,0)
    assert report['full_source_coverage'] and report['reading_cues']==27
    assert report['timeline_sha256']==sha(timeline_path)
    assert timeline==manifest['timeline']
    assert not validate_timeline(timeline,load(ROOT/'studio/studio.json')['asset_library'],require_opening=True)
    assert sha(manifest['source']['path'])==manifest['source']['sha256']
    assert sha(project['source']['path'])==project['source']['sha256']
    for asset in manifest['assets']:
        assert sha(asset['path'])==asset['sha256']
    gifs=[]
    for scene in ('dinner','child'):
        item=load(qa/(scene+'-gif-verification.json'))
        assert item['status']=='pass' and item['frames']==100 and item['duration_ms']==8000
        assert item['infinite_loop'] and item['gif_sha256']==sha(item['gif'])
        assert item['video_sha256']==sha(item['video'])
        gifs.append(item)
    assert sha(ROOT/'skills/json-asset-animation/assets/LivingSteam.tsx')==sha(ROOT/'studio/apps/video/src/LivingSteam.tsx')
    classification='2.5D living illustrations with source-anchored procedural vapor; no character-body/facial animation'
    report.update(visual_review_status='editor_frame_sequence_and_motion_checks_passed_author_review_pending',
                  visual_review_method='Opening motion study and decoded scene/GIF phase sequences, matched controls and all reading-cue contact sheets inspected; no claim of real-time playback review.',
                  animation_classification=classification,author_quality_approved=False,
                  motion_verification=str(motion_path),gif_verifications=[str(qa/(s+'-gif-verification.json')) for s in ('dinner','child')])
    save(report_path,report)
    receipt_path=base/'video/exports/com-nguoi-v5-living-illustrations-silent-review-receipt.json'
    save(receipt_path,{
        'version':timeline['version'],'status':'ready_for_review','classification':classification,
        'video':{'path':str(video),'sha256':sha(video),'bytes':video.stat().st_size},
        'gifs':[{'path':g['gif'],'sha256':g['gif_sha256'],'duration_s':8,'frames':100,'infinite_loop':True} for g in gifs],
        'script_source':manifest['source'],'canonical_source':project['source'],
        'timeline':{'path':str(timeline_path),'sha256':sha(timeline_path)},
        'motion_manifest':{'path':str(manifest_path),'sha256':sha(manifest_path)},
        'verification':{'path':str(report_path),'sha256':sha(report_path)},
        'motion_verification':{'path':str(motion_path),'sha256':sha(motion_path)},
        'sources_unchanged':True,'v4_and_earlier_reviews_preserved':True,
        'author_quality_approved':False,'public_release_approved':False,'paid_release_approved':False,
    })
    run_path=ROOT/project['run_manifest']
    run=load(run_path)
    original_flags={k:copy.deepcopy(run.get(k)) for k in (
        'author_approved','manuscript_text_approved','script_facts_approved','privacy_rights_approved',
        'founder_public_release_approved','founder_paid_release_approved','approval_gates',
        'source_facts_approval_evidence','manuscript_text_approval_evidence','script_approval_evidence')}
    active=base/'video/timeline.json'
    previous=load(active)
    if previous['version']=='v4-layer-animation':
        preserved=base/'video/timeline-v4.json'
        assert sha(active)==sha(preserved)
        for derivative in run['derivatives']:
            if Path(derivative['path'])==active:
                assert derivative['artifact_sha256']==sha(preserved)
                derivative['path']=str(preserved)
    else:
        assert previous==timeline,'Unexpected active version; review before selection.'
    save(active,timeline)
    entry=ROOT/'studio/apps/video/src/com-nguoi-v5-entry.tsx'
    project['animation_manifest']={'path':str(manifest_path),'sha256':sha(manifest_path),
                                   'render_entry':str(entry),'render_entry_sha256':sha(entry)}
    save(project_path,project)
    run['stages']['S06_audio_film']='ready_for_review'
    run['stage_evidence']['S06_audio_film']={
        'path':str(video),'artifact_sha256':sha(video),'version':timeline['version'],
        'classification':classification,'source_sha256':manifest['source']['sha256'],
        'verification':str(report_path),'motion_verification':str(motion_path),
        'gif_previews':[g['gif'] for g in gifs],'duration_s':120,'story_starts_s':10.5,'audio_tracks':0,
        'state':'V5 complete silent film and two living GIFs rendered and technically checked; exact author look/pacing approval pending.',
    }
    artifacts=[
        ('film',video),('timeline',timeline_path),('motion-manifest',manifest_path),
        ('media-qc',report_path),('motion-qc',motion_path),('receipt',receipt_path),
        ('derivation',base/'animation/v5/derivation-receipt.json'),
        ('renderer',ROOT/'studio/apps/video/src/com-nguoi-v5.tsx'),('entry',entry),
        ('steam-component',ROOT/'studio/apps/video/src/LivingSteam.tsx'),
        ('builder',base/'video/build_v5.py'),('motion-check-script',base/'video/verify_v5_motion.py'),
        ('media-check-script',base/'video/verify_silent_cut.py'),
        ('motion-study',base/'video/previews/com-nguoi-v5-opening-and-living-scene-study.mp4'),
        ('animation-skill',ROOT/'skills/json-asset-animation/SKILL.md'),
        ('gif-exporter',ROOT/'skills/json-asset-animation/scripts/export_loop_gif.py'),
    ]
    for scene,gif in zip(('dinner','child'),gifs):
        artifacts.extend([(scene+'-gif',Path(gif['gif'])),(scene+'-loop-video',Path(gif['video'])),
                          (scene+'-gif-qc',qa/(scene+'-gif-verification.json'))])
    run['derivatives']=[d for d in run['derivatives'] if not d['id'].startswith('com-nguoi-v5-')]
    for identifier,path in artifacts:
        run['derivatives'].append({'id':'com-nguoi-v5-'+identifier,'path':str(path),'artifact_sha256':sha(path),
                                  'source_sha256':manifest['source']['sha256'],'canonical_source_sha256':project['source']['sha256'],
                                  'version':timeline['version'],'format':path.suffix.lstrip('.'),'status':'ready_for_review',
                                  'rights':'Internal review; no artistic/public/paid approval inferred.','evidence':str(report_path)})
    run['next_actions'][0].update(action='Review v5 living vapor, illustration GIFs, portal landing and full-film pacing; approve the exact look or request revisions.',
                                  dependency=str(video))
    run['notes']='V5 makes both story illustrations live with curling, rising/fading vapor and periodic environmental motion; two 8-second looping GIFs accompany the full silent film. Cold bowl, family poses, complete script and portal opening preserved. V4 and earlier reviews retained; originals unchanged. Artistic/public/paid approval remains pending.'
    for key,value in original_flags.items():
        assert run.get(key)==value,'Approval scope changed: '+key
    save(run_path,run)
    print({'selected':timeline['version'],'video':str(video),'gifs':[g['gif'] for g in gifs],
           'release_approved':False,'previous_versions_preserved':True})


if __name__=='__main__':
    main()
