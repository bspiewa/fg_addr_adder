import argparse
import ipaddress


def get_cmd(range, comment, objects):
    cmd = []
    obj_name = ''
    if len(range) > 1:
        obj_name = f'{range[0]}_{range[-1]}{args.suffix}'
        cmd.append(f'edit {obj_name}')
        cmd.append(f'set range {range[0]}-{range[-1]}')
    else:
        obj_name = f'{range[0]}{args.suffix}'
        cmd.append(f'edit {obj_name}')
        cmd.append(f'set subnet {range[0]}/32')

    if comment:
        cmd.append(f'set comment "{comment}"')

    cmd.append('next')
    objects.append(obj_name)
    range.clear()
    return cmd


def underscored(text):
    return text.replace(' ', '_')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Generates script for importing IPv4 addresses to FortiGate firewalls configuration')
    parser.add_argument(
        '-s', '--suffix', help='Text at the end of the created addresses (default "_block")', default='_block', type=underscored)
    parser.add_argument(
        '-c', '--comment', help='Comment for new addresses')
    parser.add_argument(
        '-g', '--group', help='Group name for created addresses', type=underscored)

    files = parser.add_argument_group('input & output files')
    files.add_argument(
        '-i', '--input', help='Input file with IPv4 addresses list', required=True)
    files.add_argument(
        '-o', '--output', help='Output file with generated script')

    args = parser.parse_args()

    try:
        with open(args.input, 'r') as datain:
            fg_cmd = ['config firewall address']
            range = []
            objects = []
            for address in datain:
                try:
                    ip = ipaddress.ip_address(address[:-1])
                except ValueError:
                    print(f'Incorrect entry "{address[:-1]}" - skipping')
                else:
                    if range:
                        if ip - 1 not in range:
                            fg_cmd += get_cmd(range, args.comment, objects)
                    range.append(ip)
            if range:
                fg_cmd += get_cmd(range, args.comment, objects)
            fg_cmd.append('end')

            if args.group:
                fg_cmd.append(f'config firewall addrgrp')
                fg_cmd.append(f'edit {args.group}')
                fg_cmd.append('set member ' + ' '.join(obj for obj in objects))
                fg_cmd.append('next')
                fg_cmd.append('end')

            if args.output:
                with open(args.output, 'w') as dataout:
                    dataout.writelines(f'{line}\n' for line in fg_cmd)
                    print(f'File "{args.output}" was created succesfully')
            else:
                print('\n'.join(line for line in fg_cmd))

    except FileNotFoundError:
        print(f'ERROR: Unable to read file "{args.input}"')

    except PermissionError:
        print(f'ERROR: I/O problem')

    finally:
        print('Finished - press any key to exit')
        input()
