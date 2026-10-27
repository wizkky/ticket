"""Optional presentation groups; model permissions and records remain intact."""

OPTIONAL_ADMIN_MODELS = frozenset(
    {
        "ReferralApplication",
        "ReferralCode",
        "Referral",
        "ReferralPayout",
        "ReferralPayoutStatement",
        "OrganizationMember",
        "MembershipTier",
        "OrganizationMembershipRequest",
        "PotluckItem",
        "MembershipSubscriptionPlan",
        "MembershipSubscription",
        "MembershipPayment",
        "TelegramUser",
    }
)
