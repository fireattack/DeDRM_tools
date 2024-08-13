import argparse
import os

__license__ = "GPL v3"
__copyright__ = "2017-2024, John Howell <jhowell@acm.org>"

file_types = {"azw8", "kfx", "kfx-zip", "kpf"}

def cli_main(argv):
    from .kfxlib import (file_write_binary, set_logger, YJ_Book)

    log = JobLog()
    log.info("")

    allowed_exts = [".%s" % e for e in sorted(list(file_types))]
    ext_choices = ", ".join(allowed_exts[:-1] + ["or " + allowed_exts[-1]])

    parser = argparse.ArgumentParser(
            prog='calibre-debug -r "KFX Input" --',
            description="Convert KFX e-book to EPUB, PDF, CBZ or extract its resources")
    parser.add_argument("infile", help="Pathname of the %s file or notebook folder to be processed" % ext_choices)
    parser.add_argument("outfile", nargs="?", help="Optional pathname of the resulting .epub, .pdf, .cbz, or .zip file")
    parser.add_argument("-e", "--epub", action="store_true", help="Convert to EPUB (default action)")
    parser.add_argument("-2", "--epub2", action="store_true", help="Convert to EPUB 2 instead of EPUB 3")
    parser.add_argument("-p", "--pdf", action="store_true", help="Extract PDF from print replica, create PDF from comics & children's")
    parser.add_argument("-z", "--cbz", action="store_true", help="Create CBZ from print replica, comics, & children's")
    parser.add_argument("-u", "--unpack", action="store_true", help="Create a ZIP file with extracted resources")
    parser.add_argument("-j", "--json-content", action="store_true", help="Create a JSON content/position file")
    parser.add_argument("-c", "--cover", action="store_true", help="Create a generic EPUB cover page if the book does not already have one")
    args = parser.parse_args(argv[1:])

    if os.path.isfile(args.infile):
        intype = os.path.splitext(args.infile)[1]
        if intype not in allowed_exts:
            log.error("Input file must be %s" % ext_choices)
            return
    elif os.path.isdir(args.infile):
        if args.infile.endswith(".sdr"):
            log.error("Input folder must not be SDR: %s" % args.infile)
            return
    else:
        log.error("Input file does not exist: %s" % args.infile)
        return

    log.info("Processing %s" % args.infile)

    set_logger(log)
    book = YJ_Book(args.infile)
    book.decode_book(retain_yj_locals=True)

    if args.unpack:
        zip_data = book.convert_to_zip_unpack()
        output_filename = get_output_filename(args, ".zip")
        file_write_binary(output_filename, zip_data)
        log.info("KFX resources unpacked to %s" % output_filename)

    if args.json_content:
        zip_data = book.convert_to_json_content()
        output_filename = get_output_filename(args, ".json")
        file_write_binary(output_filename, zip_data)
        log.info("Created JSON content/position file %s" % output_filename)

    if args.cbz:
        if book.is_image_based_fixed_layout:
            cbz_data = book.convert_to_cbz()
            output_filename = get_output_filename(args, ".cbz")
            file_write_binary(output_filename, cbz_data)
            log.info("Converted book images to CBZ file %s" % output_filename)
        else:
            log.error("Book format does not support CBZ conversion - must be image based fixed-layout")

    if args.pdf:
        if book.is_image_based_fixed_layout:
            pdf_data = book.convert_to_pdf()
            output_filename = get_output_filename(args, ".pdf")
            file_write_binary(output_filename, pdf_data)

            if book.has_pdf_resource:
                log.info("Extracted PDF content to %s" % output_filename)
            else:
                log.info("Converted book images to PDF file %s" % output_filename)
        else:
            log.error("Book format does not support PDF conversion - must be image based fixed-layout")
    elif book.has_pdf_resource:
        log.warning("This book contains PDF content. Use the --pdf option to extract it.")

    if args.epub or args.epub2 or not (args.cbz or args.pdf or args.json_content or args.unpack):
        log.info("Converting %s to EPUB" % args.infile)
        epub_data = book.convert_to_epub(epub2_desired=args.epub2, force_cover=args.cover)
        output_filename = get_output_filename(args, ".epub")
        file_write_binary(output_filename, epub_data)
        log.info("Converted book saved to %s" % output_filename)

    set_logger()

def get_output_filename(args, extension):
    if args.outfile:
        output_filename = args.outfile
        if output_filename.lower().endswith(extension):
            output_filename = output_filename[:-len(extension)]
    else:
        output_filename = os.path.join(os.path.dirname(args.infile), os.path.splitext(os.path.basename(args.infile))[0])

    return output_filename + extension


def name_of_file(file):
    if isinstance(file, str):
        return file

    if isinstance(file, bytes):
        return repr(file)

    elif hasattr(file, "name"):
        return file.name

    return "unknown"


class JobLog(object):
    '''
    Logger that also collects errors and warnings for presentation in a job summary.
    '''

    def __init__(self, logger):
        self.logger = logger
        self.errors = []
        self.warnings = []

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.warnings.append(msg)
        self.logger.warn("WARNING: %s" % msg)

    def warning(self, desc):
        self.warn(desc)

    def error(self, msg):
        self.errors.append(msg)
        self.logger.error("ERROR: %s" % msg)

    def exception(self, msg):
        self.errors.append("EXCEPTION: %s" % msg)
        self.logger.exception("EXCEPTION: %s" % msg)

    def __call__(self, *args):
        self.info(" ".join([str(arg) for arg in args]))
