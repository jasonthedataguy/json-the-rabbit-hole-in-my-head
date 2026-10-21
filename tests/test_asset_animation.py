from pathlib import Path
import copy
import importlib.util
import tempfile
import unittest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('motion_assets', ROOT / 'skills/json-asset-animation/scripts/motion_assets.py')
motion = importlib.util.module_from_spec(spec)
spec.loader.exec_module(motion)


class AnimationSkillTests(unittest.TestCase):
    def setUp(self):
        cache = ROOT / 'studio/.cache/tests'
        cache.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=cache)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.library = self.root / 'art'
        self.library.mkdir()
        self.image = self.library / 'layer.png'
        im = Image.new('RGBA', (24, 24), (0, 0, 0, 0))
        im.paste((90, 120, 80, 255), (4, 4, 20, 20))
        im.save(self.image)
        self.source = self.root / 'script.md'
        self.source.write_text('# Cơm nguội\n\nAn exact story.\n', encoding='utf-8')
        layer = {'id': 'leaf', 'asset_id': 'art', 'x': 5, 'y': 5, 'width': 24, 'height': 24, 'z': 1, 'tracks': {'rotation': [{'t': 0, 'value': -1}, {'t': 2, 'value': 1}, {'t': 4, 'value': -1}]}}
        second = copy.deepcopy(layer)
        second.update({'id': 'paper', 'z': 2, 'x': 45, 'tracks': {'x': [{'t': 0, 'value': 45}, {'t': 3, 'value': 53}, {'t': 5, 'value': 46}]}})
        self.data = {'schema_version': '1.0', 'story_slug': 'com-nguoi', 'classification': 'layer_animation', 'source': {'path': str(self.source), 'sha256': motion.sha(self.source)}, 'width': 100, 'height': 180, 'fps': 30, 'duration_s': 10, 'opening': {'title': 'Cơm nguội', 'portal_asset': 'art', 'reveal_asset': 'art', 'focus_x': .5, 'focus_y': .5, 'title_hold_s': 1, 'entry_end_s': 2, 'story_start_s': 3}, 'assets': [{'id': 'art', 'path': str(self.image), 'sha256': motion.sha(self.image), 'role': 'cutout'}], 'layers': [layer, second], 'audio': {'mode': 'silent'}, 'author_quality_approved': False, 'public_release_approved': False, 'paid_release_approved': False}

    def check(self):
        return motion.check_manifest(self.data, [self.library])

    def test_independent_object_motion_passes_preflight(self):
        self.assertEqual(self.check()['errors'], [])

    def test_static_scene_and_camera_text_only_are_rejected(self):
        for layer in self.data['layers']:
            layer['tracks'] = {}
        self.data['camera'] = {'zoom': [1, 2]}
        self.data['title_animation'] = True
        self.assertTrue(any('independently' in e for e in self.check()['errors']))

    def test_identical_movement_with_different_initial_offsets_is_lockstep(self):
        for index, layer in enumerate(self.data['layers']):
            layer['tracks'] = {'x': [{'t': 0, 'value': 10 + index * 20}, {'t': 2, 'value': 20 + index * 20}]}
        self.assertTrue(any('lockstep' in e for e in self.check()['errors']))

    def test_invisible_or_offcanvas_motion_does_not_count(self):
        self.data['layers'][0]['tracks']['opacity'] = [{'t': 0, 'value': 0}, {'t': 4, 'value': 0}]
        self.assertTrue(self.check()['errors'])
        self.data['layers'][0]['tracks'].pop('opacity')
        self.data['layers'][0]['x'] = 200
        self.assertTrue(self.check()['errors'])

    def test_opaque_images_cannot_masquerade_as_clean_cutouts(self):
        Image.new('RGB', (24,24), 'white').save(self.image)
        self.data['assets'][0]['sha256'] = motion.sha(self.image)
        self.assertTrue(any('no transparent' in e for e in self.check()['errors']))

    def test_stale_and_private_assets_are_rejected(self):
        self.data['assets'][0]['sha256'] = 'stale'
        self.assertTrue(any('stale' in e for e in self.check()['errors']))
        other = self.root / 'private.png'
        Image.new('RGB', (8,8), 'black').save(other)
        self.data['assets'][0].update({'path': str(other), 'sha256': motion.sha(other)})
        self.assertTrue(any('trusted' in e for e in self.check()['errors']))

    def test_intro_cannot_disappear_or_precede_title_hold(self):
        self.data['opening']['story_start_s'] = 0
        self.assertTrue(any('hold title' in e for e in self.check()['errors']))

    def test_title_and_source_drift_are_rejected(self):
        self.data['opening']['title'] = 'An invented heading'
        self.assertTrue(any('source heading' in e for e in self.check()['errors']))
        self.source.write_text('Changed', encoding='utf-8')
        self.assertTrue(any('source' in e for e in self.check()['errors']))

    def test_invalid_keyframe_order_and_unimplemented_audio_are_rejected(self):
        self.data['layers'][0]['tracks']['rotation'].reverse()
        self.data['audio']['mode'] = 'author_recording'
        result = self.check()
        self.assertTrue(any('increase' in e for e in result['errors']))
        self.assertTrue(any('audio' in e for e in result['errors']))

    def test_motion_file_cannot_grant_release_approval(self):
        self.data['public_release_approved'] = True
        self.assertTrue(any('cannot grant' in e for e in self.check()['errors']))

    def test_inspection_and_staging_preserve_original_bytes(self):
        before = motion.sha(self.image)
        self.assertGreater(motion.inspect(self.image)['transparent_fraction'], 0)
        destination = self.root / 'cache/image.png'
        motion.stage_file(self.image, destination)
        self.assertEqual(motion.sha(destination), before)
        self.assertEqual(motion.sha(self.image), before)


if __name__ == '__main__':
    unittest.main()
