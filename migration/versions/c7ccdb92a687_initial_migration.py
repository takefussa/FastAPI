"""Initial migration

Revision ID: c7ccdb92a687
Revises: 50615d0341b9
Create Date: 2025-01-23 07:43:58.512337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7ccdb92a687'
down_revision: Union[str, None] = '50615d0341b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('projects', 'description')

    # Add 'name' column with a temporary default value
    op.add_column('tasks', sa.Column('name', sa.String(), nullable=False, server_default='Unnamed Task'))

    # Remove the temporary default value
    op.alter_column('tasks', 'name', server_default=None)

    op.alter_column('tasks', 'project_id',
                    existing_type=sa.INTEGER(),
                    nullable=False)
    op.create_foreign_key(None, 'tasks', 'projects', ['project_id'], ['id'])
    op.drop_column('tasks', 'title')
    op.drop_column('tasks', 'priority')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('priority', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('tasks', sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.alter_column('tasks', 'project_id',
                    existing_type=sa.INTEGER(),
                    nullable=True)
    op.drop_column('tasks', 'name')
    op.add_column('projects', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
