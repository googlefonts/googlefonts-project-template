from babelfont import Babelfont
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(prog="babelfont", description='Convert between font formats')
    parser.add_argument('input', metavar='IN', help="Input file")
    parser.add_argument('output', metavar='OUT', help="Output file")
    args = parser.parse_args()

    try:
      font = Babelfont.load(args.input)
    except Exception as e:
      print("Couldn't read %s: %s" % (args.input, e))
      sys.exit(1)

    try:
      font.save(args.output)
    except Exception as e:
      print("Couldn't write %s: %s" % (args.output, e))
      raise e
      sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    sys.exit(main())
