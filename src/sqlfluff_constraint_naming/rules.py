"""Rules for enforcing constraint naming conventions."""

from typing import Optional

from sqlfluff.core.rules import BaseRule, LintResult, RuleContext
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


class Rule_CN01(BaseRule):
    """
    Constraint names should use appropriate prefixes.

    PRIMARY KEY constraints should use "pk_" prefix.
    FOREIGN KEY constraints should use "fk_" prefix.
    CHECK constraints should use "chk_" prefix.
    UNIQUE constraints should use "uc_" prefix.
    DEFAULT constraints should use "df_" prefix.

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

    name = "custom.constraint_naming"
    description = "Enforces naming conventions for SQL constraints, ensuring they start with the appropriate prefixes."
    groups = ("all", "custom", "convention")
    crawl_behaviour = SegmentSeekerCrawler({"naked_identifier", "object_reference"})

    # These are the expected prefixes for each constraint type
    _PREFIX_MAPPINGS = {
        "DEFAULT": "df_",
        "PRIMARY": "pk_",
        "FOREIGN": "fk_",
        "UNIQUE": "uc_",
        "CHECK": "chk_",
    }

    def _eval(self, context: RuleContext) -> Optional[LintResult]:
        """Validate constraint name prefixes.

        Look for constraint declarations and validate that the constraint
        name follows the naming convention.
        """
        try:
            segment = context.segment
            # Check if we have a constraint name by looking at the parent segment
            is_constraint_name = False

            # Get the parent and check if it has a keyword before this segment
            parent = context.parent_stack[-1] if context.parent_stack else None
            if parent:
                # Check for a simple case - this segment is preceded by the CONSTRAINT keyword
                for i, child in enumerate(parent.segments):
                    if child is segment and i > 0:
                        # Look at previous segment(s)
                        prev_idx = i - 1
                        while prev_idx >= 0:
                            prev = parent.segments[prev_idx]
                            if prev.is_type("keyword") and prev.raw.upper() == "CONSTRAINT":
                                is_constraint_name = True
                                self.logger.debug(f"Found constraint name: {segment.raw}")
                                break
                            elif not prev.is_type("whitespace"):
                                break
                            prev_idx -= 1
                        break

            if is_constraint_name:
                # Get the constraint name
                constraint_name = segment.raw.lower()
                self.logger.debug(f"Processing constraint name: {constraint_name}")

                # Find the constraint type by looking ahead
                constraint_type = None
                # Look at siblings in the parent segment
                if parent:
                    for i, child in enumerate(parent.segments):
                        if child is segment:
                            # Found our segment, look ahead
                            idx = i + 1
                            while idx < len(parent.segments):
                                next_seg = parent.segments[idx]
                                if next_seg.is_type("keyword") and next_seg.raw.upper() in self._PREFIX_MAPPINGS:
                                    constraint_type = next_seg.raw.upper()
                                    self.logger.debug(f"Found constraint type: {constraint_type}")
                                    break
                                # If we encounter a segment that's not whitespace and not a keyword,
                                # and it's not what we're looking for, continue searching
                                elif not (next_seg.is_type("whitespace") or next_seg.is_type("keyword")):
                                    # We may have passed the relevant segment
                                    if idx - i > 5:  # If we've looked ahead more than 5 segments, stop
                                        self.logger.debug("Looked ahead more than 5 segments, stopping search")
                                        break
                                idx += 1
                            break

                if constraint_type:
                    expected_prefix = self._PREFIX_MAPPINGS.get(constraint_type)
                    self.logger.debug(f"Expected prefix: {expected_prefix}")
                    if expected_prefix and not constraint_name.startswith(expected_prefix):
                        self.logger.debug(f"Constraint name '{constraint_name}' violates naming convention")
                        return LintResult(
                            anchor=segment,
                            description=(
                                f"Constraint name '{constraint_name}' should start with "
                                f"'{expected_prefix}' for {constraint_type} constraints."
                            )
                        )
                else:
                    self.logger.debug("No constraint type found")
            return None
        except Exception as e:
            self.logger.error(f"Exception in constraint naming rule: {str(e)}", )
            return None
