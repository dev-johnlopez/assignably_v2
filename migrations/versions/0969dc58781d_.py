"""empty message

Revision ID: 0969dc58781d
Revises: 
Create Date: 2019-01-03 13:32:34.399216

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0969dc58781d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('line_1', sa.String(length=255), nullable=True),
    sa.Column('line_2', sa.String(length=255), nullable=True),
    sa.Column('line_3', sa.String(length=255), nullable=True),
    sa.Column('line_4', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=255), nullable=True),
    sa.Column('state_code', sa.String(length=2), nullable=True),
    sa.Column('postal_code', sa.String(length=20), nullable=True),
    sa.Column('county', sa.String(length=255), nullable=True),
    sa.Column('country', sa.String(length=255), nullable=True),
    sa.Column('latitude', sa.Numeric(precision=9, scale=6), nullable=True),
    sa.Column('longitude', sa.Numeric(precision=9, scale=6), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_Address_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_Address_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('current_login_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_ip', sa.String(length=40), nullable=True),
    sa.Column('current_login_ip', sa.String(length=40), nullable=True),
    sa.Column('login_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('contact',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('contact_type', sa.String(length=50), nullable=True),
    sa.Column('phone', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('mailing_address_id', sa.Integer(), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_Contact_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['mailing_address_id'], ['address.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_Contact_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.Float(), nullable=True),
    sa.Column('payload_json', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_name'), 'notification', ['name'], unique=False)
    op.create_index(op.f('ix_notification_timestamp'), 'notification', ['timestamp'], unique=False)
    op.create_table('property',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.Column('property_type', sa.Integer(), nullable=True),
    sa.Column('units', sa.Integer(), nullable=True),
    sa.Column('sq_feet', sa.Integer(), nullable=True),
    sa.Column('bedrooms', sa.Integer(), nullable=True),
    sa.Column('bathrooms', sa.Integer(), nullable=True),
    sa.Column('basement_desc', sa.String(length=255), nullable=True),
    sa.Column('garage_desc', sa.String(length=255), nullable=True),
    sa.Column('last_sale_date', sa.Date(), nullable=True),
    sa.Column('owner_occupied', sa.Boolean(), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], ),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_Property_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_Property_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('task',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('complete', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_name'), 'task', ['name'], unique=False)
    op.create_table('note',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('comments', sa.String(length=5000), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_Note_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_Note_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('proforma',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('arv', sa.Integer(), nullable=True),
    sa.Column('purchase_price', sa.Integer(), nullable=True),
    sa.Column('seller_concessions', sa.Integer(), nullable=True),
    sa.Column('closing_costs', sa.Integer(), nullable=True),
    sa.Column('rent_ready_costs', sa.Integer(), nullable=True),
    sa.Column('initial_reserve_amount', sa.Integer(), nullable=True),
    sa.Column('lease_option_fee', sa.Integer(), nullable=True),
    sa.Column('total_finished_sq_foot', sa.Integer(), nullable=True),
    sa.Column('land_value_perc', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('income_tax_rate', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('vacancy_perc', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_Proforma_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['property_id'], ['property.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_Proforma_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('property_contact',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_PropertyContact_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['property_id'], ['property.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_PropertyContact_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('line_item',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('income_proforma_id', sa.Integer(), nullable=True),
    sa.Column('expense_proforma_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(length=255), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('frequency', sa.Integer(), nullable=True),
    sa.Column('annual_increase_perc', sa.Numeric(precision=6, scale=2), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_LineItem_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['expense_proforma_id'], ['proforma.id'], ),
    sa.ForeignKeyConstraint(['income_proforma_id'], ['proforma.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_LineItem_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('loan',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('proforma_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('interest_rate', sa.Numeric(precision=6, scale=3), nullable=True),
    sa.Column('interest_only', sa.Boolean(), nullable=True),
    sa.Column('length', sa.Integer(), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_Loan_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['proforma_id'], ['proforma.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_Loan_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('property_contact_role',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('property_contact_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('updated_by_id', sa.Integer(), nullable=True),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_PropertyContactRole_created_by_id', use_alter=True),
    sa.ForeignKeyConstraint(['property_contact_id'], ['property_contact.id'], ),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name='fk_PropertyContactRole_updated_by_id', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('property_contact_role')
    op.drop_table('loan')
    op.drop_table('line_item')
    op.drop_table('property_contact')
    op.drop_table('proforma')
    op.drop_table('note')
    op.drop_index(op.f('ix_task_name'), table_name='task')
    op.drop_table('task')
    op.drop_table('roles_users')
    op.drop_table('property')
    op.drop_index(op.f('ix_notification_timestamp'), table_name='notification')
    op.drop_index(op.f('ix_notification_name'), table_name='notification')
    op.drop_table('notification')
    op.drop_table('contact')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('address')
    # ### end Alembic commands ###