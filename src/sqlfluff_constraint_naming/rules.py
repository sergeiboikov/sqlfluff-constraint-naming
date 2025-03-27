"""Rules for enforcing constraint naming conventions."""

from typing import Optional, List, Type

from sqlfluff.core.rules import BaseRule, LintResult, RuleContext
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler
from sqlfluff.core.plugin import hookimpl


@hookimpl
def get_rules() -> List[Type[BaseRule]]:
    """Get plugin rules.

    Returns:
        A list of rule classes to be registered with SQLFluff.
    """
    return [Rule_CRCN01]


class Rule_CRCN01(BaseRule):
    """
    Constraint names should use appropriate prefixes.

    PRIMARY KEY constraints should use 'pk_' prefix.
    FOREIGN KEY constraints should use 'fk_' prefix.
    CHECK constraints should use 'chk_' prefix.
    UNIQUE constraints should use 'uc_' prefix.

    **Anti-pattern**

    .. code-block:: sql

        CREATE TABLE person (
            person_id INT,
            email VARCHAR,
            CONSTRAINT person_pk PRIMARY KEY (person_id),
            CONSTRAINT email_unique UNIQUE (email)
        );

    **Best practice**

    .. code-block:: sql

        CREATE TABLE person (
            person_id INT,
            email VARCHAR,
            CONSTRAINT pk_person PRIMARY KEY (person_id),
            CONSTRAINT uc_email UNIQUE (email)
        );
    """

    groups = ("all", "core", "convention")
    crawl_behaviour = SegmentSeekerCrawler({"constraint_name"})

    # These are the expected prefixes for each constraint type
    _PREFIX_MAPPINGS = {
        "PRIMARY KEY": "pk_",
        "FOREIGN KEY": "fk_",
        "UNIQUE": "uc_",
        "CHECK": "chk_",
    }

    def _eval(self, context: RuleContext) -> Optional[LintResult]:
        """Validate constraint name prefixes.

        Look for constraint declarations and validate that the constraint
        name follows the naming convention.
        """
        segment = context.segment

        # We're looking for a constraint name (identifier) followed by a constraint type
        if segment.is_type("constraint_name"):
            # Get the constraint name
            constraint_name = segment.raw.lower()

            # Find the constraint type by looking ahead
            constraint_type = None
            current_segment = segment
            # Limit our search to 10 segments (to avoid an infinite loop)
            for _ in range(10):
                if not current_segment.get_next():
                    break
                current_segment = current_segment.get_next()

                if (current_segment.is_type("keyword") and current_segment.raw.upper() in self._PREFIX_MAPPINGS):
                    constraint_type = current_segment.raw.upper()
                    break
                elif current_segment.is_type("foreign_key_reference"):
                    constraint_type = "FOREIGN KEY"
                    break

            if constraint_type:
                expected_prefix = self._PREFIX_MAPPINGS.get(constraint_type)
                if expected_prefix and not constraint_name.startswith(expected_prefix):
                    return LintResult(
                        anchor=segment,
                        description=(
                            f"Constraint name '{constraint_name}' should start with "
                            f"'{expected_prefix}' for {constraint_type} constraints."
                        )
                    )

        return None
