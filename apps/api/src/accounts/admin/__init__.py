"""Accounts admin package.

Split into submodules to keep each file under the 1000-line limit.
All admin classes are imported here so Django's autodiscovery finds them.
"""

from accounts.admin.billing import UserBillingProfileAdmin as UserBillingProfileAdmin
from accounts.admin.moderation import (
    GlobalBanAdmin as GlobalBanAdmin,
)
from accounts.admin.moderation import (
    ImpersonationLogAdmin as ImpersonationLogAdmin,
)
from accounts.admin.referral import (
    ReferralAdmin as ReferralAdmin,
)
from accounts.admin.referral import (
    ReferralCodeAdmin as ReferralCodeAdmin,
)
from accounts.admin.referral import (
    ReferralPayoutAdmin as ReferralPayoutAdmin,
)
from accounts.admin.referral import (
    ReferralPayoutStatementAdmin as ReferralPayoutStatementAdmin,
)
from accounts.admin.referral_application import ReferralApplicationAdmin as ReferralApplicationAdmin
from accounts.admin.tracking import (
    EmailVerificationReminderTrackingAdmin as EmailVerificationReminderTrackingAdmin,
)
from accounts.admin.user import (
    RevelUserAdmin as RevelUserAdmin,
)
from accounts.admin.user import (
    UserDataExportAdmin as UserDataExportAdmin,
)
