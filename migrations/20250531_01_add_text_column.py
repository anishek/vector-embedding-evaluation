"""add text column to e5_large_instruct table
-- depends: 20250530_01_SS41k
"""

from yoyo import step

__depends__ = {"20250530_01_create_table_for_e5_model_embedding"}

steps = [
    step(
        "ALTER TABLE e5_large_instruct ADD COLUMN text_content text not null",
        "ALTER TABLE e5_large_instruct DROP COLUMN text_content",
    )
]
