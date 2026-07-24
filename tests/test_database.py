import os
import sqlite3
import tempfile
import unittest
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import database

class DatabaseTests(unittest.TestCase):
    def test_create_and_save_high_score(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "scores.db")
            database.create_scores_table(db_path)
            database.save_score("ana", 10, db_path)
            database.save_score("beto", 25, db_path)
            database.save_score("cata", 15, db_path)
            database.save_score("dani", 20, db_path)
            database.save_score("eva", 30, db_path)
            database.save_score("fede", 29, db_path)
            database.save_score("gabi", 35, db_path)

            self.assertTrue(database.check_if_table_exists(db_path))
            self.assertEqual(database.get_highest_score(db_path), 35)
            self.assertEqual(database.get_highscore_name(db_path), "gabi")

            with sqlite3.connect(db_path) as conn:
                rows = conn.execute("SELECT name, score FROM scores ORDER BY score DESC").fetchall()
            self.assertEqual(rows, [("gabi", 35), ("eva", 30), ("beto", 25), ("ana", 10)])

if __name__ == "__main__":
    unittest.main()
