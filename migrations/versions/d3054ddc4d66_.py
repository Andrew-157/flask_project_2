"""empty message

Revision ID: d3054ddc4d66
Revises: 93c045532aae
Create Date: 2023-08-28 09:12:24.544317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3054ddc4d66'
down_revision = '93c045532aae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tagged_recommendations', schema=None) as batch_op:
        batch_op.drop_constraint('tagged_recommendations_recommendation_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('tagged_recommendations_tag_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'recommendation', ['recommendation_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'tag', ['tag_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tagged_recommendations', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('tagged_recommendations_tag_id_fkey', 'tag', ['tag_id'], ['id'])
        batch_op.create_foreign_key('tagged_recommendations_recommendation_id_fkey', 'recommendation', ['recommendation_id'], ['id'])

    # ### end Alembic commands ###
