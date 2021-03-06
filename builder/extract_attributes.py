
import argparse
import pandas as pd

# see GENERIC_DB.md for output file formats

def extract_attribute_groups(input_file, output_file, organism_id):
    data = pd.read_csv(input_file, sep='\t', header=0, index_col=0)

    data['ORGANISM_ID'] = organism_id
    data['CODE'] = data['name']

    data.to_csv(output_file, sep='\t',
                columns=['ORGANISM_ID', 'name', 'CODE', 'desc', 'linkout_label', 'linkout_url',
                      'default_selected', 'pub_name', 'pub_url'],
                header=False, index=True)


def extract_attributes(input_files, groups_file, output_file, organism_id,
                       key_lstrip=None, key_rstrip=None):

    groups = pd.read_csv(groups_file, sep='\t', header=0, index_col=0)
    assert groups.index.name == 'id'

    all_attributes = []

    for input_file in input_files:

        # find id corresponding to file
        dataset_key = input_file
        if key_lstrip and dataset_key.startswith(key_lstrip):
            dataset_key = dataset_key[len(key_lstrip):]
        if key_rstrip and dataset_key.endswith(key_rstrip):
            dataset_key = dataset_key[:-len(key_rstrip)]

        matched = groups[groups['dataset_key'] == dataset_key].index

        if len(matched) == 0:
            raise Exception('Group file has no id: %s' % input_file)
        elif len(matched) > 2:
            raise Exception('Group file has multiple ids (expected 1): %s' % input_file)

        group_id = matched[0]

        attributes = pd.read_csv(input_file, sep='\t', header=False,
                            names=['NAME', 'DESCRIPTION'],
                            dtype='str', na_filter=False)

        attributes['ATTRIBUTE_GROUP_ID'] = group_id
        attributes['ORGANISM_ID'] = organism_id
        attributes['EXTERNAL_ID'] = attributes['NAME']

        all_attributes.append(attributes)

    all_attributes = pd.concat(all_attributes)
    all_attributes.index.name = 'ID'

    all_attributes.to_csv(output_file, sep='\t', header=False, index=True,
                          columns=['ORGANISM_ID', 'ATTRIBUTE_GROUP_ID', 'EXTERNAL_ID', 'NAME', 'DESCRIPTION'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create attribute files in generic_db format')
    subparsers = parser.add_subparsers(dest='subparser_name')

    # attribute groups
    parser_attribute_groups = subparsers.add_parser('attribute_groups')
    parser_attribute_groups.add_argument('organism_id', help='organism id')
    parser_attribute_groups.add_argument('output', help='output file')
    parser_attribute_groups.add_argument('input', help='table of attribute group metadata')

    # attributes
    parser_attributes = subparsers.add_parser('attributes')
    parser_attributes.add_argument('organism_id', help='organism id')
    parser_attributes.add_argument('output', help='output file')
    parser_attributes.add_argument('groups', help='table of attribute group metadata')
    parser_attributes.add_argument('inputs', help='something', nargs='+')
    parser_attributes.add_argument('--key_lstrip', type=str,
                                   help='remove given string from left of filename to compute dataset key')
    parser_attributes.add_argument('--key_rstrip', type=str,
                                   help='remove given string from right of filename to compute dataset key')

    # parse args and dispatch
    args = parser.parse_args()

    if args.subparser_name == 'attribute_groups':
        extract_attribute_groups(args.input, args.output, args.organism_id)
    elif args.subparser_name == 'attributes':
        extract_attributes(args.inputs, args.groups, args.output, args.organism_id,
                           args.key_lstrip, args.key_rstrip)
    else:
        raise Exception('unexpected command')