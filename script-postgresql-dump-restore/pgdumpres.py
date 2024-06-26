#!/usr/bin/env python3

import argparse
import subprocess
import sys
import getpass

# Function to run commands and control errors
def run_command(command, success_message):
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Error: Command failed with return code {result.returncode}")
        sys.exit(1)
    else:
        print(success_message)

# Function to dump roles
def dumpRoles(user, password, host):
    filename = f"backup_roles_{host}.sql"
    command = f"PGPASSWORD={password} pg_dumpall -r --no-role-passwords -h {host} -U {user} > {filename}"
    run_command(command, "Roles dump completed successfully")

    # Modify the file to remove unwanted words
    try:
        with open(filename, 'r') as file:
            content = file.read()

        content = content.replace("NOBYPASSRLS", "").replace("NOSUPERUSER", "").replace("  ", " ").replace(" ;", ";")

        with open(filename, 'w') as file:
            file.write(content)

        print(f"Roles dump completed and unwanted words removed from {filename}. Check roles prior restore.")

    except Exception as e:
        print(f"An error occurred while modifying the file: {e}")

# Function to dump databases
def dumpFull(user, password, host, db):
    filename = f"backup_full_{host}_{db}.dump"
    command = f"PGPASSWORD={password} pg_dump -O -h {host} -U {user} -d {db} -f {filename}"
    run_command(command, "Full database dump completed successfully")

# Function to dump databases compressed
def dumpFullCompress(user, password, host, db):
    filename = f"backup_full_compressed_{host}_{db}.dump"
    command = f"PGPASSWORD={password} pg_dump -O -Fc -h {host} -U {user} -d {db} -f {filename}"
    run_command(command, "Compressed full database dump completed successfully")

# Function to dump whole schemas
def dumpSchema(user, password, host, db):
    filename = f"backup_schema_{host}_{db}.dump"
    command = f"PGPASSWORD={password} pg_dump -O -s -h {host} -U {user} -d {db} -f {filename}"
    run_command(command, "Schema dump completed successfully")

    # Modify the file to remove unwanted words
    try:
        with open(filename, 'r') as file:
            content = file.read()

        content = content.replace("DEFAULT NULL::character varying", "DEFAULT NULL")

        with open(filename, 'w') as file:
            file.write(content)

        print(f"Schema dump completed and unwanted words removed from {filename}")
        
    except Exception as e:
        print(f"An error occurred while modifying the file: {e}")

# Function to restore uncompressed files with psql, indicated for roles, schemas and small DB dumps
def restore(user, password, host, db, dumpFile):
    command = f"PGPASSWORD={password} psql -h {host} -U {user} -d {db}-f {dumpFile}"
    run_command(command, "Restore completed successfully")

# Function to restore compressed files with pg_restore, best solution for massive DB dumps
def restoreCompress(user, password, host, db, dumpFile):
    command = f"PGPASSWORD={password} pg_restore -h {host} -U {user} -d {db} -Fc {dumpFile}"
    run_command(command, "Compressed restore completed successfully")

def main():

    examples = """\
Examples:
  Dump roles:
    python pgdumpres.py --host 127.0.0.1 --user myuser --dumpRole

  Dump full database:
    python pgdumpres.py --host 127.0.0.1 --user myuser --db mydb --dumpFull

  Dump compressed full database:
    python pgdumpres.py --host 127.0.0.1 --user myuser --db mydb --dumpFullCompress

  Dump schema:
    python pgdumpres.py --host 127.0.0.1 --user myuser --db mydb --dumpSchema

  Restore from uncompressed file:
    python pgdumpres.py --host 127.0.0.1 --user myuser --db mydb --dumpFile backup_file.sql --restore

  Restore from compressed file:
    python pgdumpres.py --host 127.0.0.1 --user myuser --db mydb --dumpFile backup_file.dump --restoreCompress
"""

    parser = argparse.ArgumentParser(
        description="PostgreSQL Database dump & restore script",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--host", required=True, help="Host name or IP address of the database server")
    parser.add_argument("--user", required=True, help="Database user")
    parser.add_argument("--password", help="Database password (optional, if not provided it will be requested interactively)")
    parser.add_argument("--db", help="Database name (required for dumpFull, dumpFullCompress, dumpSchema dumps, restore and restoreCompress)")
    parser.add_argument("--dumpFile", help="Dump filename for restoration (required for restore and restoreCompress)")
    parser.add_argument("--dumpFull", action='store_true', help="Dump the database schema & data")
    parser.add_argument("--dumpRole", action='store_true', help="Dump the roles")
    parser.add_argument("--dumpSchema", action='store_true', help="Dump the schema")
    parser.add_argument("--dumpFullCompress", action='store_true', help="Dump the database schema & data compressed")
    parser.add_argument("--restore", action='store_true', help="Restore uncompressed files with psql, indicated for roles, schemas and small DB dumps")
    parser.add_argument("--restoreCompress", action='store_true', help="Restore compressed files with pg_restore, best solution for massive DB dumps")

    # Define variables
    args = parser.parse_args()
    dump_actions = [args.dumpFull, args.dumpRole, args.dumpSchema, args.dumpFullCompress]
    restore_actions = [args.restore, args.restoreCompress]
    
    # Check that a action parameter is pased
    if sum(dump_actions) + sum(restore_actions) == 0:
        print("Error: You must provide at least one of --dumpFull, --dumpRole, --dumpSchema, --dumpFullCompress, --restore, or --restoreCompress.")
        sys.exit(1)

    # Check that a dump and restore actions parameters are not combined
    if sum(dump_actions) > 0 and sum(restore_actions) > 0:
        print("Error: You cannot combine dump and restore actions in the same execution.")
        sys.exit(1)

    # Request password interactively if not provided
    if not args.password:
        args.password = getpass.getpass(prompt='Database password: ')

    # Check that only one of dumpFull, dumpRole, dumpSchema, dumpFullCompress is provided
    if sum(dump_actions) > 1:
        print("Error: You must provide exactly one of --dumpFull, --dumpFullCompress, --dumpRole or --dumpSchema.")
        sys.exit(1)

    # Check that only one of restore, restoreCompress is provided
    if sum(restore_actions) > 1:
        print("Error: You must provide exactly one of --restore or --restoreCompress.")
        sys.exit(1)

    # Ensure db is provided when required
    if (args.dumpFull or args.dumpSchema or args.dumpFullCompress or args.restore or args.restoreCompress) and not args.db:
        print("Error: --db is required when using --dumpFull, --dumpSchema, --dumpFullCompress, --restore or --restoreCompress.")
        sys.exit(1)

    # Ensure dumpFile is provided when required
    if (args.restore or args.restoreCompress) and not args.dumpFile:
        print("Error: --dumpFile is required when using --restore or --restoreCompress.")
        sys.exit(1)

    # Execute the appropriate function based on the arguments
    if args.dumpRole:
        dumpRoles(args.user, args.password, args.host)
    elif args.dumpFull:
        dumpFull(args.user, args.password, args.host, args.db)
    elif args.dumpFullCompress:
        dumpFullCompress(args.user, args.password, args.host, args.db)
    elif args.dumpSchema:
        dumpSchema(args.user, args.password, args.host, args.db)
    elif args.restore:
        restore(args.user, args.password, args.host, args.db, args.dumpFile)
    elif args.restoreCompress:
        restoreCompress(args.user, args.password, args.host, args.db, args.dumpFile)

if __name__ == "__main__":
    main()
