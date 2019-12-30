
import re

from box import Box
from gssutils import pathify

from validator.helpers.reference import get_cogs_implied_resources
from validator.helpers.csv import get_csv_as_pandas
from validator.helpers.json import get_json_as_dict
from validator.cacher import cache

def compare_components_and_columns_for_reference_repos_used_by_schema(validator, schema, **kwargs):

    """
    Validates a csv file used for columns reference data

    :param validator:
    :param schema:
    :param kwargs:
    :return:
    """

    paths_to_components_files = [x for x in get_cogs_implied_resources(schema, validator.local_ref) if x.endswith("components.csv")]

    for path in paths_to_components_files:
        compare_components_csv_with_columns_csv(validator, path)

@cache
def compare_components_csv_with_columns_csv(validator, comp_path):

    col_path = comp_path.replace("components.csv", "columns.csv")

    comp_df = get_csv_as_pandas(comp_path, "get components file '{}' as pandas dataframe".format(comp_path))
    col_df = get_csv_as_pandas(col_path, "get components file '{}' as pandas dataframe".format(col_path))

    # TODO - these checks are similar, we should be able to wrap and repeat with different args

    # ---------------------------
    # Check component attachments
    attached = {
        "Measure": "qb:measure",
        "Dimension": "qb:dimension",
        "Attribute": "qb:attribute"
    }

    for attachment, as_qb in attached.items():

        m_df = comp_df[comp_df["Component Type"] == attachment]
        for i, row in m_df.iterrows():

            # Every row label in components, should match a title in columns.csv
            if row["Label"] not in col_df["title"].unique():
                validator.results.add_result("The label '{}' in components.csv, should appear in columns.csv but it does"
                                             " not.".format(row["Label"]), {"columns file": col_path, "component path": comp_path,
                                                      "component row": i})
            else:
                # We have an appropriately named row in columns.csv, now we need to check it
                col_row_dict = Box(col_df[col_df["title"] == row["Label"]].to_dict(orient='records')[0])

                # Confirm that if' its a measure in one, it's a measure in the other
                if col_row_dict["component_attachment"] != as_qb:
                    validator.results.add_result("The component '{}' on row '{}' is of type '{}' and should"
                                            " be attached as a '{}' in the columns file. But we have '{}'."
                                                .format(col_row_dict.title,i, attachment, as_qb, col_row_dict.component_attachment),
                                            {"component_file": comp_path, "column_file": col_path})


def compare_components_and_codelist_metadata_for_reference_repos_used_by_schema(validator, schema, **kwargs):

    """
    Validates componets file codelist entries against codelist-metadata json

    :param validator:
    :param schema:
    :param kwargs:
    :return:
    """

    paths_to_components_files = [x for x in get_cogs_implied_resources(schema, validator.local_ref) if x.endswith("components.csv")]

    for path in paths_to_components_files:
        compare_components_csv_with_codelists_metadata(validator, path)


@cache
def compare_components_csv_with_codelists_metadata(validator, comp_path):

    comp_df = get_csv_as_pandas(comp_path, "get components file '{}' as pandas dataframe".format(comp_path))

    codelist_metadata_path = comp_path.replace("components.csv", "codelists-metadata.json")
    codelist_metadata = get_json_as_dict(codelist_metadata_path, "getting codelist metadata from '{}'"
                                         .format(codelist_metadata_path))

    codelist_labels = [x["rdfs:label"] for x in codelist_metadata["tables"]]
    codelist_reference = {}
    for label in codelist_labels:
        codelist_reference.update({"http://gss-data.org.uk/def/concept-scheme/{}"
        .format(pathify(label)): label})

    for i, row in comp_df.iterrows():

        codelist_entry = row["Codelist"]

        if not isinstance(codelist_entry, str):
            continue

        if codelist_entry.startswith("'http://gss-data.org.uk/"):

            if codelist_entry not in codelist_reference.keys():
                validator.results.add_result("The component entry for column entry Codelist: '{}' does"
                                             "not appear in the associated coelist metadata file."
                                             .format(codelist_entry), {"specified_codelists": codelist_reference})
