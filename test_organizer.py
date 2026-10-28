import tempfile
import unittest
from pathlib import Path

import organizer as org


class OrganizerTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self._tmp.name).resolve()

    def tearDown(self):
        self._tmp.cleanup()

    def make(self, *names):
        for n in names:
            (self.folder / n).write_text("x")

    def test_category_is_case_insensitive(self):
        self.assertEqual(org.category_for(Path("A.PNG")), "Images")
        self.assertEqual(org.category_for(Path("noext")), "Other")

    def test_plan_skips_hidden_files_and_folders(self):
        self.make("a.txt", ".hidden")
        (self.folder / "sub").mkdir()
        self.assertEqual([s.name for s, _ in org.plan(self.folder)], ["a.txt"])

    def test_name_clash_never_overwrites(self):
        self.make("b.pdf")
        (self.folder / "Documents").mkdir()
        (self.folder / "Documents" / "b.pdf").write_text("old")
        org.apply_moves(org.plan(self.folder))
        self.assertEqual((self.folder / "Documents" / "b.pdf").read_text(), "old")
        self.assertTrue((self.folder / "Documents" / "b (1).pdf").exists())

    def test_apply_then_undo_restores_everything(self):
        self.make("a.png", "b.pdf")
        org.save_log(self.folder, org.apply_moves(org.plan(self.folder)))
        org.undo(self.folder)
        self.assertTrue((self.folder / "a.png").exists())
        self.assertTrue((self.folder / "b.pdf").exists())
        self.assertFalse((self.folder / "Images").exists())

    def test_two_runs_can_both_be_undone(self):
        self.make("a.png")
        org.save_log(self.folder, org.apply_moves(org.plan(self.folder)))
        self.make("b.png")
        org.save_log(self.folder, org.apply_moves(org.plan(self.folder)))
        org.undo(self.folder)
        self.assertTrue((self.folder / "a.png").exists())
        self.assertTrue((self.folder / "b.png").exists())


if __name__ == "__main__":
    unittest.main()
