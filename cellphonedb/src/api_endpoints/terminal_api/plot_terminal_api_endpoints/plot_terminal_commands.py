import sys
import traceback

import click

from cellphonedb.src.app.app_logger import app_logger
from cellphonedb.src.exceptions.MissingR import MissingR
from cellphonedb.src.exceptions.RRuntimeException import RRuntimeException
from cellphonedb.src.plotters import r_plotter

try:
    r_plotter.ensure_R_setup()
except MissingR:
    print('As there is no R environment set up, some functionalities will be disabled, e.g. plot')


@click.command()
@click.option('--means-path', type=click.Path(exists=True, file_okay=True, dir_okay=False),
              default='./out/means.txt', help='Analysis output means [./out/means.txt]')
@click.option('--pvalues-path', type=click.Path(exists=True, file_okay=True, dir_okay=False),
              default='./out/pvalues.txt', help='Analysis output pvalues [./out/pvalues.txt]')
@click.option('--output-path', type=click.Path(exists=True, file_okay=False, writable=True),
              default='./out', help='Path to write generated plot [./out]')
@click.option('--output-name', type=str, default='./plot.pdf', help='Output file with plot [plot.pdf]')
@click.option('--rows', type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='List of rows to plot, one per line [all available]')
@click.option('--columns', type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='List of columns to plot, one per line [all available]')
@click.option('--verbose/--quiet', default=True, help='Print or hide cellphonedb logs [verbose]')
def dot_plot(means_path: str, pvalues_path: str, output_path: str, output_name: str, rows: str,
             columns: str, verbose: bool):
    try:
        r_plotter.dot_plot(means_path, pvalues_path, output_path, output_name, rows, columns)
    except MissingR:
        print('You cannot perform this plot command unless there is a working R setup according to CellPhoneDB specs')
    except RRuntimeException as e:
        app_logger.error(str(e))
    except:
        app_logger.error('Unexpected error')

        if verbose:
            traceback.print_exc(file=sys.stdout)
        else:
            app_logger.error('execute with --verbose to see full stack trace')


@click.command()
@click.argument('meta-path', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('--pvalues-path', type=click.Path(exists=True, file_okay=True, dir_okay=False),
              default='./out/pvalues.txt', help='Analysis output pvalues [./out/pvalues.txt]')
@click.option('--output-path', type=click.Path(exists=True, file_okay=False, writable=True),
              default='./out', help='Path to write generated plot [./out]')
@click.option('--count-name', type=str, default='heatmap_count.pdf',
              help='Output file with count plot [heatmap_count.pdf]')
@click.option('--log-name', type=str, default='heatmap_log_count.pdf',
              help='Output file with log count plot [heatmap_log_count.pdf]')
@click.option('--verbose/--quiet', default=True, help='Print or hide cellphonedb logs [verbose]')
def heatmap_plot(meta_path: str, pvalues_path: str, output_path: str, count_name: str, log_name: str, verbose: bool):
    try:
        r_plotter.heatmaps_plot(meta_path, pvalues_path, output_path, log_name, count_name)
    except MissingR:
        print('You cannot perform this plot command unless there is a working R setup according to CellPhoneDB specs')
    except RRuntimeException as e:
        app_logger.error(str(e))
    except:
        app_logger.error('Unexpected error')

        if verbose:
            traceback.print_exc(file=sys.stdout)
        else:
            app_logger.error('execute with --verbose to see full stack trace')
