# SQLFluff Constraint Naming Plugin

A SQLFluff plugin to enforce constraint naming conventions according to the Postgres SQL Format Guidelines.

## Rules Implemented

- **CN01** - Constraint names should use appropriate prefixes:
  - PRIMARY KEY constraints should use `pk_` prefix
  - FOREIGN KEY constraints should use `fk_` prefix
  - CHECK constraints should use `chk_` prefix
  - UNIQUE constraints should use `uc_` prefix

## Installation

1. Clone the repository.

2. Install the plugin:

```bash
# Navigate to the plugin directory
cd D:/GitHub/sqlfluff-constraint-naming

# Install the plugin in development mode
pip install -e .
```

2. Verify that SQLFluff recognizes the plugin:

```bash
sqlfluff rules
```

You should see the `CN01` rule listed among the available rules.

## Usage

Once installed, the plugin automatically integrates with SQLFluff. Just run SQLFluff as usual:

```bash
sqlfluff lint path/to/your/sql/files
```

## Examples

The following examples demonstrate how the constraint naming rules are enforced:

### Incorrect constraint naming:

```sql
CREATE TABLE person (
    person_id INT,
    email TEXT,
    CONSTRAINT person_pk PRIMARY KEY (person_id),
    CONSTRAINT email_unique UNIQUE (email)
);
```

### Correct constraint naming:

```sql
CREATE TABLE person (
    person_id INT,
    email TEXT,
    CONSTRAINT pk_person PRIMARY KEY (person_id),
    CONSTRAINT uc_email UNIQUE (email)
);
```