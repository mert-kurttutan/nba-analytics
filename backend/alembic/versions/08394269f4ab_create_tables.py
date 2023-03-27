"""create tables

Revision ID: 08394269f4ab
Revises: 
Create Date: 2023-03-21 17:44:25.677833

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '08394269f4ab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_client',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('trusted', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('api_key', sqlmodel.sql.sqltypes.AutoString(length=512), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=256), nullable=False),
    sa.Column('admin_email', sqlmodel.sql.sqltypes.AutoString(length=256), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.Column('frontend_type', sqlmodel.sql.sqltypes.AutoString(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_api_client_api_key'), 'api_client', ['api_key'], unique=True)
    op.create_table('gamelog',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('DAY_WITHIN_SEASON', sa.Integer(), nullable=False),
    sa.Column('GAME_DATE', sa.Date(), nullable=False),
    sa.Column('GAME_ID', sa.Integer(), nullable=False),
    sa.Column('T1_IS_HOME', sa.Boolean(), nullable=False),
    sa.Column('T1_PLUS_MINUS', sa.Float(), nullable=False),
    sa.Column('T1_PTS', sa.Float(), nullable=False),
    sa.Column('T1_TEAM_ID', sa.Integer(), nullable=False),
    sa.Column('T1_TEAM_NAME', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('T1_W', sa.Float(), nullable=False),
    sa.Column('T1_W_cum', sa.Float(), nullable=False),
    sa.Column('T2_IS_HOME', sa.Boolean(), nullable=False),
    sa.Column('T2_PLUS_MINUS', sa.Float(), nullable=False),
    sa.Column('T2_PTS', sa.Float(), nullable=False),
    sa.Column('T2_TEAM_ID', sa.Integer(), nullable=False),
    sa.Column('T2_TEAM_NAME', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('T2_W', sa.Float(), nullable=False),
    sa.Column('T2_W_cum', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teamstat',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('DAY_WITHIN_SEASON', sa.Integer(), nullable=False),
    sa.Column('GAME_DATE', sa.Date(), nullable=False),
    sa.Column('TEAM_ID', sa.Integer(), nullable=False),
    sa.Column('lag08_GP', sa.Float(), nullable=False),
    sa.Column('lag08_W_PCT', sa.Float(), nullable=False),
    sa.Column('lag08_FG_PCT', sa.Float(), nullable=False),
    sa.Column('lag08_FT_PCT', sa.Float(), nullable=False),
    sa.Column('lag08_OREB', sa.Float(), nullable=False),
    sa.Column('lag08_DREB', sa.Float(), nullable=False),
    sa.Column('lag08_REB', sa.Float(), nullable=False),
    sa.Column('lag08_AST', sa.Float(), nullable=False),
    sa.Column('lag08_TOV', sa.Float(), nullable=False),
    sa.Column('lag08_STL', sa.Float(), nullable=False),
    sa.Column('lag08_BLK', sa.Float(), nullable=False),
    sa.Column('lag08_PTS', sa.Float(), nullable=False),
    sa.Column('lag08_PLUS_MINUS', sa.Float(), nullable=False),
    sa.Column('lag08_W_PCT_RANK', sa.Float(), nullable=False),
    sa.Column('lag08_PTS_RANK', sa.Float(), nullable=False),
    sa.Column('lag08_PLUS_MINUS_RANK', sa.Float(), nullable=False),
    sa.Column('lag16_GP', sa.Float(), nullable=False),
    sa.Column('lag16_W_PCT', sa.Float(), nullable=False),
    sa.Column('lag16_FG_PCT', sa.Float(), nullable=False),
    sa.Column('lag16_FT_PCT', sa.Float(), nullable=False),
    sa.Column('lag16_OREB', sa.Float(), nullable=False),
    sa.Column('lag16_DREB', sa.Float(), nullable=False),
    sa.Column('lag16_REB', sa.Float(), nullable=False),
    sa.Column('lag16_AST', sa.Float(), nullable=False),
    sa.Column('lag16_TOV', sa.Float(), nullable=False),
    sa.Column('lag16_STL', sa.Float(), nullable=False),
    sa.Column('lag16_BLK', sa.Float(), nullable=False),
    sa.Column('lag16_PTS', sa.Float(), nullable=False),
    sa.Column('lag16_PLUS_MINUS', sa.Float(), nullable=False),
    sa.Column('lag16_W_PCT_RANK', sa.Float(), nullable=False),
    sa.Column('lag16_PTS_RANK', sa.Float(), nullable=False),
    sa.Column('lag16_PLUS_MINUS_RANK', sa.Float(), nullable=False),
    sa.Column('lag32_GP', sa.Float(), nullable=False),
    sa.Column('lag32_W_PCT', sa.Float(), nullable=False),
    sa.Column('lag32_FG_PCT', sa.Float(), nullable=False),
    sa.Column('lag32_FT_PCT', sa.Float(), nullable=False),
    sa.Column('lag32_OREB', sa.Float(), nullable=False),
    sa.Column('lag32_DREB', sa.Float(), nullable=False),
    sa.Column('lag32_REB', sa.Float(), nullable=False),
    sa.Column('lag32_AST', sa.Float(), nullable=False),
    sa.Column('lag32_TOV', sa.Float(), nullable=False),
    sa.Column('lag32_STL', sa.Float(), nullable=False),
    sa.Column('lag32_BLK', sa.Float(), nullable=False),
    sa.Column('lag32_PTS', sa.Float(), nullable=False),
    sa.Column('lag32_PLUS_MINUS', sa.Float(), nullable=False),
    sa.Column('lag32_W_PCT_RANK', sa.Float(), nullable=False),
    sa.Column('lag32_PTS_RANK', sa.Float(), nullable=False),
    sa.Column('lag32_PLUS_MINUS_RANK', sa.Float(), nullable=False),
    sa.Column('lag64_GP', sa.Float(), nullable=False),
    sa.Column('lag64_W_PCT', sa.Float(), nullable=False),
    sa.Column('lag64_FG_PCT', sa.Float(), nullable=False),
    sa.Column('lag64_FT_PCT', sa.Float(), nullable=False),
    sa.Column('lag64_OREB', sa.Float(), nullable=False),
    sa.Column('lag64_DREB', sa.Float(), nullable=False),
    sa.Column('lag64_REB', sa.Float(), nullable=False),
    sa.Column('lag64_AST', sa.Float(), nullable=False),
    sa.Column('lag64_TOV', sa.Float(), nullable=False),
    sa.Column('lag64_STL', sa.Float(), nullable=False),
    sa.Column('lag64_BLK', sa.Float(), nullable=False),
    sa.Column('lag64_PTS', sa.Float(), nullable=False),
    sa.Column('lag64_PLUS_MINUS', sa.Float(), nullable=False),
    sa.Column('lag64_W_PCT_RANK', sa.Float(), nullable=False),
    sa.Column('lag64_PTS_RANK', sa.Float(), nullable=False),
    sa.Column('lag64_PLUS_MINUS_RANK', sa.Float(), nullable=False),
    sa.Column('lag180_GP', sa.Float(), nullable=False),
    sa.Column('lag180_W_PCT', sa.Float(), nullable=False),
    sa.Column('lag180_FG_PCT', sa.Float(), nullable=False),
    sa.Column('lag180_FT_PCT', sa.Float(), nullable=False),
    sa.Column('lag180_OREB', sa.Float(), nullable=False),
    sa.Column('lag180_DREB', sa.Float(), nullable=False),
    sa.Column('lag180_REB', sa.Float(), nullable=False),
    sa.Column('lag180_AST', sa.Float(), nullable=False),
    sa.Column('lag180_TOV', sa.Float(), nullable=False),
    sa.Column('lag180_STL', sa.Float(), nullable=False),
    sa.Column('lag180_BLK', sa.Float(), nullable=False),
    sa.Column('lag180_PTS', sa.Float(), nullable=False),
    sa.Column('lag180_PLUS_MINUS', sa.Float(), nullable=False),
    sa.Column('lag180_W_PCT_RANK', sa.Float(), nullable=False),
    sa.Column('lag180_PTS_RANK', sa.Float(), nullable=False),
    sa.Column('lag180_PLUS_MINUS_RANK', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('enabled', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    sa.Column('notes', sqlmodel.sql.sqltypes.AutoString(length=1024), server_default='', nullable=False),
    sa.Column('deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('show_on_leaderboard', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    sa.Column('streak_last_day_date', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('last_activity_date', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('tos_acceptance_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(length=128), nullable=False),
    sa.Column('auth_method', sqlmodel.sql.sqltypes.AutoString(length=128), nullable=False),
    sa.Column('display_name', sqlmodel.sql.sqltypes.AutoString(length=256), nullable=False),
    sa.Column('api_client_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('streak_days', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['api_client_id'], ['api_client.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_display_name_id', 'user', ['display_name', 'id'], unique=True)
    op.create_index('ix_user_username', 'user', ['api_client_id', 'username', 'auth_method'], unique=True)
    op.create_table('account',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('provider', sqlmodel.sql.sqltypes.AutoString(length=128), nullable=False),
    sa.Column('provider_account_id', sqlmodel.sql.sqltypes.AutoString(length=128), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('provider', 'account', ['provider_account_id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('provider', table_name='account')
    op.drop_table('account')
    op.drop_index('ix_user_username', table_name='user')
    op.drop_index('ix_user_display_name_id', table_name='user')
    op.drop_table('user')
    op.drop_table('teamstat')
    op.drop_table('gamelog')
    op.drop_index(op.f('ix_api_client_api_key'), table_name='api_client')
    op.drop_table('api_client')
    # ### end Alembic commands ###