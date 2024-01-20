from typing import Sequence
from pathlib import Path
from dataclasses import dataclass, field

from loguru import logger

from lib.domain.webinar.models import Account
from lib.domain.contacts.models import VCard
from lib.domain.contacts.repository import VCardRepository


@dataclass(frozen=True, slots=True)
class ContactService:
    vcard_repo: VCardRepository = field(default_factory=VCardRepository)

    def create_vcard(self, account: Account, group: str) -> VCard:
        return VCard(
            last_name=f"{account.name} {account.family_name}",
            first_name=group,
            email=account.email,
            phone=account.phone,
            organisation=group,
        )

    def save_accounts_to_file(
            self,
            accounts: Sequence[Account],
            group: str,
    ) -> Path:
        logger.debug(f"Saving {len(accounts)} accounts to file")
        vcards = [self.create_vcard(account, group) for account in accounts]
        path = self.vcard_repo.save_vcards_to_file(vcards, group)
        logger.debug(f"Saved accounts to {path}")
        return path
