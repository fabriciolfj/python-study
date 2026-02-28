from dataclasses import dataclass


@dataclass
class DefaultHistory:
    hasRecentDefault: bool
    defaultCount: int
    maxDelayDays: int
    hasActiveRestrictions: bool


@dataclass
class CreditInfo:
    monthyIncome: float
    currentDebtRatio: float
    creditScore: int
    defaultHistory: DefaultHistory

    @staticmethod
    def from_dict(data: dict) -> "CreditInfo":
        return CreditInfo(
            monthyIncome=data["monthlyIncome"],
            currentDebtRatio=data["currentDebtRatio"],
            creditScore=data["creditScore"],
            defaultHistory=DefaultHistory(
                hasRecentDefault=data["defaultHistory"]["hasRecentDefault"],
                defaultCount=data["defaultHistory"]["defaultCount"],
                maxDelayDays=data["defaultHistory"]["maxDelayDays"],
                hasActiveRestrictions=data["defaultHistory"]["hasActiveRestrictions"])
        )