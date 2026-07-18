"""change student dob to date
Revision ID: 1659c01b0eeb
Revises: d945ce3cec30
Create Date: 2026-07-18 15:20:00.351933
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '1659c01b0eeb'
down_revision: Union[str, Sequence[str], None] = 'd945ce3cec30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_foreign_key(None, 'attendance', 'students', ['student_id'], ['id'])
    op.create_foreign_key(None, 'class_schedules', 'staff', ['staff_id'], ['id'])
    op.create_foreign_key(None, 'daily_logs', 'staff', ['staff_id'], ['id'])
    op.drop_constraint(op.f('parents_user_id_fkey'), 'parents', type_='foreignkey')
    op.create_foreign_key(None, 'parents', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_column('payments', 'razorpay_signature')
    op.drop_constraint(op.f('staff_accounts_user_id_fkey'), 'staff_accounts', type_='foreignkey')
    op.create_foreign_key(None, 'staff_accounts', 'staff', ['staff_id'], ['id'])
    op.create_foreign_key(None, 'staff_accounts', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.alter_column('staff_courses', 'assigned_date',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column('staff_courses', 'monthly_salary',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key(None, 'staff_courses', 'staff', ['staff_id'], ['id'])
    op.alter_column('student_courses', 'joined_date',
               existing_type=sa.DATE(),
               nullable=False)
    op.create_foreign_key(None, 'student_courses', 'students', ['student_id'], ['id'])
    op.execute("ALTER TABLE students ALTER COLUMN dob TYPE DATE USING to_date(dob, 'MM/DD/YYYY')")
    op.alter_column('students', 'dob', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE students ALTER COLUMN dob TYPE VARCHAR USING to_char(dob, 'MM/DD/YYYY')")
    op.drop_constraint(None, 'student_courses', type_='foreignkey')
    op.alter_column('student_courses', 'joined_date',
               existing_type=sa.DATE(),
               nullable=True)
    op.drop_constraint(None, 'staff_courses', type_='foreignkey')
    op.alter_column('staff_courses', 'monthly_salary',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('staff_courses', 'assigned_date',
               existing_type=sa.DATE(),
               nullable=True)
    op.drop_constraint(None, 'staff_accounts', type_='foreignkey')
    op.drop_constraint(None, 'staff_accounts', type_='foreignkey')
    op.create_foreign_key(op.f('staff_accounts_user_id_fkey'), 'staff_accounts', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.add_column('payments', sa.Column('razorpay_signature', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'parents', type_='foreignkey')
    op.create_foreign_key(op.f('parents_user_id_fkey'), 'parents', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'daily_logs', type_='foreignkey')
    op.drop_constraint(None, 'class_schedules', type_='foreignkey')
    op.drop_constraint(None, 'attendance', type_='foreignkey')
