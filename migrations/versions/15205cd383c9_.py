"""empty message

Revision ID: 15205cd383c9
Revises: cff6e367bad9
Create Date: 2022-05-22 16:34:07.928583

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15205cd383c9'
down_revision = 'cff6e367bad9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cheese', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_attribution', sa.String(length=128)))
        batch_op.add_column(sa.Column('info_link', sa.String(length=256)))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cheese', schema=None) as batch_op:
        batch_op.drop_column('info_link')
        batch_op.drop_column('image_attribution')

    # ### end Alembic commands ###
