import numpy as np
import pymodaq.utils.math_utils

from pymodaq_utils.utils import ThreadCommand
from pymodaq_data.data import DataToExport, Axis
from pymodaq_gui.parameter import Parameter

from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
from pymodaq.utils.data import DataFromPlugins

from pymodaq_plugins_teaching.daq_viewer_plugins.plugins_1D.daq_1Dviewer_Spectrometer import DAQ_1DViewer_Spectrometer
from pymodaq_plugins_teaching.hardware.spectrometer import Spectrometer

# TODO:
# (1) change the name of the following class to DAQ_1DViewer_TheNameOfYourChoice
# (2) change the name of this file to daq_1Dviewer_TheNameOfYourChoice ("TheNameOfYourChoice" should be the SAME
#     for the class name and the file name.)
# (3) this file should then be put into the right folder, namely IN THE FOLDER OF THE PLUGIN YOU ARE DEVELOPING:
#     pymodaq_plugins_my_plugin/daq_viewer_plugins/plugins_1D


class DAQ_1DViewer_Spectrometer_advanced(DAQ_1DViewer_Spectrometer):

    def grab_data(self, Naverage=1, **kwargs):
        """Start a grab from the detector

        Parameters
        ----------
        Naverage: int
            Number of hardware averaging (if hardware averaging is possible, self.hardware_averaging should be set to
            True in class preamble and you should code this implementation)
        kwargs: dict
            others optionals arguments
        """
        # Check what the new dimension of x_axis
        data_x_axis = self.controller.get_wavelength_axis()
        self.x_axis = Axis(data=data_x_axis, label='wavelength', units='nm', index=0)

        data_tot = self.controller.grab_spectrum()
        self.dte_signal.emit(DataToExport(
            'myplugin',
            data=[DataFromPlugins(
                name='Mock1',
                data=[data_tot],
                dim='Data1D',
                labels=['spectrum'],
                axes=[self.x_axis])
            ])
        )

        data_tot = self.controller.grab_spectrum()
        data_m = pymodaq.utils.math_utils.my_moment(self.x_axis, data_tot)

        self.dte_signal.emit(DataToExport(
            'myplugin',
            data=[DataFromPlugins(
                name='Standard deviation',
                data=data_m,
                dim='Data0D',
                labels=['spectrum']
            )
            ])
        )


if __name__ == '__main__':
    main(__file__)
