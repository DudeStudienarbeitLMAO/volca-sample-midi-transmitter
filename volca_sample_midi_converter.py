import mido
import argparse
import sys

def transmit_midi(input_number=0, output_number=1):
    with mido.open_input(input_number) as inport:
        with mido.open_output(output_number) as outport:
            for msg in inport:
                print(msg)
                if msg.type is 'note_on':
                    cc_msg = mido.Message('control_change', control=43, value=msg.note)
                    outport.send(msg)
                    outport.send(cc_msg)
                else:
                    outport.send(msg)

def list_midi_devices():
    print('Found the following devices/ports:')
    for num, device in enumerate(mido.get_input_names()):
        print("Device Number " + str(num) + ": %s" % device)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Takes midi input and adds Volca Sample control_change messages to play chromatically')
    parser.add_argument('--inport', '-i', type=int, help='the input port')
    parser.add_argument('--outport', '-o', type=int, help='the output port')
    parser.add_argument('--list', '-l', action='store_true', help='lists all available midi devices and ports')
    args = parser.parse_args()
    if args.list:
        list_midi_devices()
        sys.exit(0)
    if not (args.inport and args.outport):
        if len(mido.get_input_names()) < 2:
            print("Not enough devices to route! Exiting.")
            exit(-1)
        else:
            transmit_midi()
    elif (args.inport and args.outport):
        transmit_midi(args.inport, args.outport)