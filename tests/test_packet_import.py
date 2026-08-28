"""Smoke tests for VERA packet runtime."""
from pathlib import Path
import ast


def test_packet_module_parses():
    src = Path("vera_packet_v0_3.py").read_text(encoding="utf-8")
    ast.parse(src)
    assert "class" in src or "def " in src


def test_checkout_parses():
    src = Path("payment/checkout.py").read_text(encoding="utf-8")
    ast.parse(src)
