"""
Unit tests for CodeExample.py (Contact Book).
Compliant with PEP8 and PEP287.
Tests edge cases: Unicode, long strings, infinities, empty, and invalid input.
"""
import unittest
from unittest.mock import patch
import builtins
import math

import CodeExample as ce

class TestContactBook(unittest.TestCase):
    def setUp(self):
        self.contacts = [
            {"name": "Alice", "phone": "123", "email": "alice@example.com"},
            {"name": "张伟", "phone": "456", "email": "zhangwei@example.cn"},
            {"name": "محمد", "phone": "789", "email": "mohammad@example.com"},
            {"name": "A" * 10000, "phone": "999", "email": "longname@example.com"},
            {"name": "Inf", "phone": str(float('inf')), "email": "inf@example.com"},
            {"name": "NegInf", "phone": str(float('-inf')), "email": "neginf@example.com"},
        ]

    def test_view_contacts_empty(self):
        with patch("builtins.print") as mock_print:
            ce.view_contacts([])
            mock_print.assert_any_call("\nℹ️ Your contact book is empty.")

    def test_view_contacts_various(self):
        with patch("builtins.print") as mock_print:
            ce.view_contacts(self.contacts)
            self.assertTrue(any("张伟" in str(call) for call in mock_print.call_args_list))
            self.assertTrue(any("محمد" in str(call) for call in mock_print.call_args_list))
            self.assertTrue(any("A" * 100 in str(call) for call in mock_print.call_args_list))
            self.assertTrue(any("inf" in str(call).lower() for call in mock_print.call_args_list))

    def test_add_contact_unicode_long_inf(self):
        test_cases = [
            ("张伟", "456", "zhangwei@example.cn"),
            ("محمد", "789", "mohammad@example.com"),
            ("A" * 10000, "999", "longname@example.com"),
            ("Inf", str(float('inf')), "inf@example.com"),
            ("NegInf", str(float('-inf')), "neginf@example.com"),
        ]
        for name, phone, email in test_cases:
            with patch("builtins.input", side_effect=[name, phone, email]), \
                 patch("builtins.print") as mock_print:
                contacts = ce.add_contact([])
                self.assertEqual(contacts[0]["name"], name)
                self.assertEqual(contacts[0]["phone"], phone)
                self.assertEqual(contacts[0]["email"], email)
                self.assertTrue(any("Success" in str(call) for call in mock_print.call_args_list))

    def test_search_contact_case_insensitive(self):
        with patch("builtins.input", return_value="alice"), \
             patch("builtins.print") as mock_print:
            ce.search_contact(self.contacts)
            self.assertTrue(any("Alice" in str(call) for call in mock_print.call_args_list))

    def test_search_contact_unicode(self):
        with patch("builtins.input", return_value="张"), \
             patch("builtins.print") as mock_print:
            ce.search_contact(self.contacts)
            self.assertTrue(any("张伟" in str(call) for call in mock_print.call_args_list))
        with patch("builtins.input", return_value="محمد"), \
             patch("builtins.print") as mock_print:
            ce.search_contact(self.contacts)
            self.assertTrue(any("محمد" in str(call) for call in mock_print.call_args_list))

    def test_search_contact_long_string(self):
        long_search = "A" * 10000
        with patch("builtins.input", return_value=long_search), \
             patch("builtins.print") as mock_print:
            ce.search_contact(self.contacts)
            self.assertTrue(any(long_search in str(call) for call in mock_print.call_args_list))

    def test_search_contact_inf(self):
       with patch("builtins.input", return_value="inf"), \
           patch("builtins.print") as mock_print:
          ce.search_contact(self.contacts)
          self.assertTrue(any("Inf" in str(call) for call in mock_print.call_args_list))

       with patch("builtins.input", return_value="-inf"), \
           patch("builtins.print") as mock_print:
          ce.search_contact(self.contacts)
          self.assertTrue(any("NegInf" in str(call) or "-inf" in str(call) for call in mock_print.call_args_list))

    def test_search_contact_empty(self):
        with patch("builtins.print") as mock_print:
            ce.search_contact([])
            mock_print.assert_any_call("\nℹ️ Your contact book is empty. Nothing to search.")

    def test_add_contact_empty_fields(self):
        with patch("builtins.input", side_effect=["", "", ""]), \
             patch("builtins.print") as mock_print:
            contacts = ce.add_contact([])
            self.assertEqual(contacts[0]["name"], "")
            self.assertEqual(contacts[0]["phone"], "")
            self.assertEqual(contacts[0]["email"], "")
            self.assertTrue(any("Success" in str(call) for call in mock_print.call_args_list))

    def test_invalid_menu_choice(self):
        with patch("builtins.input", side_effect=["5", "4"]), \
             patch("builtins.print") as mock_print:
            with patch("CodeExample.display_menu"), patch("CodeExample.add_contact"), patch("CodeExample.view_contacts"), patch("CodeExample.search_contact"):
                ce.main()
            self.assertTrue(any("Invalid choice" in str(call) for call in mock_print.call_args_list))

if __name__ == "__main__":
    unittest.main()
