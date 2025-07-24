"""
Data models for the Money Tracker Bot
"""

from dataclasses import dataclass


@dataclass
class Expense:
    amount: float
    category: str
    account: str
    name: str
    date: str


@dataclass
class Income:
    amount: float
    category: str
    account: str
    name: str
    date: str


@dataclass
class Transfer:
    amount: float
    from_account: str
    to_account: str
    description: str
    date: str
