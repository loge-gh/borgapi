"""Test deff command"""
from .test_01_borgapi import BorgapiTests


class DiffTests(BorgapiTests):
    """Diff command tests"""

    def setUp(self):
        super().setUp()
        self._create_default()

    def test_01_add_file(self):
        """Diff new file"""
        with open(self.file_3, "w") as fp:
            fp.write(self.file_3_text)
        self.api.create(f"{self.repo}::2", self.data)
        output = self.api.diff(self.archive, "2", json_lines=True)
        self.assertType(output, list)
        modify_path = None
        modify_type = None
        for item in output:
            for item2 in item["changes"]:
                if item2.get("type") == "added":
                    modify_path = item["path"]
                    modify_type = "added"
                    break
        self.assertEqual(modify_path, self.file_3, "Unexpected new filename")
        self.assertEqual(modify_type, "added", "New file not listed as added")

    def test_02_modify_file(self):
        """Diff modified file"""
        with open(self.file_3, "w") as fp:
            fp.write(self.file_3_text)
        with open(self.file_2, "w") as fp:
            fp.write(self.file_3_text)
        self.api.create(f"{self.repo}::2", self.data)
        output = self.api.diff(self.archive, "2", json_lines=True, sort=True)
        self.assertType(output, list)
        modify_path = None
        modify_type = None
        for item in output:
            for item2 in item["changes"]:
                if item2.get("type") == "modified":
                    modify_path = item["path"]
                    modify_type = "modified"
                    break
        self.assertEqual(modify_path, self.file_2, "Unexpected file changed")
        self.assertEqual(modify_type, "modified", "Unexpected change type")

    def test_03_output(self):
        """Diff string"""
        with open(self.file_3, "w") as fp:
            fp.write(self.file_3_text)
        self.api.create(f"{self.repo}::2", self.data)
        output = self.api.diff(self.archive, "2")
        self._display("diff sting", output)
        self.assertType(output, str)

    def test_04_output_json(self):
        """Diff json"""
        with open(self.file_3, "w") as fp:
            fp.write(self.file_3_text)
        self.api.create(f"{self.repo}::2", self.data)
        output = self.api.diff(self.archive, "2", log_json=True)
        self._display("diff log json", output)
        self.assertAnyType(output, str)
