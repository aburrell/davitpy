#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# rad_tdiff.py, Angeline G. Burrell (AGB), UoL
#
# Comments: Class for tdiff values
#-----------------------------------------------------------------------------
'''Define and retrieve transmission frequency bands for the SuperDARN radars.

Classes
----------------------------------------------------------------------------
radTdiff
----------------------------------------------------------------------------

Moduleauthor
------------
Angeline G. Burrell (AGB), 26 August 2016, University of Leicester (UoL)
'''
import logging
import os
import numpy as np
import datetime as dt

#-----------------------------------------------------------------------------
class radTdiff(object):
    '''Contains the time and frequency dependent radar phase calibration (tdiff)

    Parameters
    ------------
    rad : (str or int)
        3-character radar code or numerical ID number
    tdiff_file : (str or None)
        File containing tdiff estimates, if None the hardware file is used.
        (default=None)
    tdiff_col : (int or None)
        File column number containing the tdiff estimate (zero offset)
        (default=None)
    terr_col : (int or None)
        File column number containing the tdiff uncertainty (zero offset)
        (default=None)
    tband_col : (int or None)
        File column number containing transmission frequency band (zero offset)
        (default=None)
    val_col : (int or None)
        File column number containing validation flag (zero offset)
        (default=None)
    stime_cols : (list of int or None)
        File numbers containing strings that will be formated into start times
        (zero offset) (default=None)
    etime_cols : (list of int or None)
        File numbers containing strings that will be formated into end times
        (zero offset) (default=None)
    time_fmt : (str or None)
        String to cast starting and ending time strings as a datetime object
    hsplit : (str or NoneType)
        Character seperating data labels in header.  None splits on all
        whitespace characters. (default=None)


    Attributes
    ------------
    tdiff_file : (str)
        File containing tdiff estimates
    rad_code : (str)
        Radar 3-character code (lowercase only)
    stid : (int)
        Radar numerical ID
    tbands : (list of integers)
        List of transmision frequency band numbers
    stimes : (list of datetimes)
        List of starting times
    etimes : (list of datetimes)
        List of ending times
    est_tdiffs : (list of floats)
        List of tdiff estimates (microseconds)
    tdiff_errs : (list of floats)
        List of tdiff estimate uncertainties (microseconds)
    validated : (list of bool)
        List of flags declaring whether or not the tdiff estimate was validated

    Methods
    ---------
    get_tdiff
    load_tdiff

    written by AGB 26/08/16
    '''

    def __init__(self, rad, tdiff_file=None, tdiff_col=None, terr_col=None,
                 tband_col=None, val_col=None, stime_cols=None, etime_cols=None,
                 time_fmt=None, split_col=None):
        import davitpy.pydarn.radar.tdiff.rad_freqbands as rad_freqbands
        
        # Assign the radar IDs
        if rad_freqbands.id_to_code.has_key(rad):
            self.rad_code = rad_freqbands.id_to_code[rad]
            self.stid = rad
        else:
            self.rad_code = rad
            self.stid = None

            for stid in rad_freqbands.id_to_code.keys():
                if rad_freqbands.id_to_code[stid] == rad.lower():
                    self.stid = stid
                    break

        if self.rad_code is None or self.stid is None:
            logging.error("unknown radar [{:}]".format(rad))
            self.tdiff_file = None
        else:
            # Ensure the specified tdiff file is valid
            self.tdiff_file = tdiff_file

            if tdiff_file is not None and not os.path.isfile(tdiff_file):
                self.tdiff_file = None

        # Load the tdiff lists
        self.tbands = list()
        self.stimes = list()
        self.etimes = list()
        self.est_tdiffs = list()
        self.tdiff_errs = list()
        self.validated = list()

        if tdiff_file is None:
            self.load_hardware_tdiff()
        elif self.tdiff_file is not None:
            self.load_tdiff(tdiff_col, terr_col, tband_col, val_col, stime_cols,
                            etime_cols, time_fmt, split_col=split_col)

        return

    def __str__(self):
        '''Object string representation

        Parameters
        ----------
        None

        Returns
        --------
        ostr : (str)
            Formatted output denoting the radar, the number of frequency bands,
            and the frequency bands in MHz

        Example
        --------
        In[1]: tdiff = rad_tdiff.radTdiff(10., "han.tdiff")
        In[2]: print tdiff
        Radar transmission frequency bands:
            Code: han       ID: 10
            Filename: han.tdiff
            Number of tdiff estimates spanning 1995-11-13 to 1999-05-30: 17
                Band Start_Time End_Time Validated TDIFF TDIFF_Err (microsec)
        '''
        ostr = "Radar transmission frequency bands:\n"
        # Add radar name
        ostr = "{:s}\tCode: {:}\tID: {:}\n".format(ostr, self.rad_code,
                                                   self.stid)
        ostr = "{:s}\tFilename: {:}\n".format(ostr, self.tdiff_file)

        # If there isn't any data, say so.  Otherwise print it.
        if len(self.tbands) == 0:
            ostr = "{:s}\tUnable to load data\n".format(ostr)
        else:
            # Add number of frequency bands
            ostr = "{:s}\tNumber of tdiff estimates spanning ".format(ostr)
            ostr = "{:s}{:}-{:}: {:d}\n".format(ostr, min(self.stimes).date(),
                                                max(self.etimes).date(),
                                                len(self.tbands))
            # Add the tdiff estimates
            ostr = "{:s}\tBand Start_Time End_Time Validated".format(ostr)
            ostr = "{:s} TDIFF TDIFF_Err (microsec)\n".format(ostr)
            for i,v in enumerate(self.validated):
                ostr = "{:s}\t{:02d} {:} {:} {:} {:.6f} {:.6f}\n".format(ostr, \
                            self.tbands[i], self.stimes[i], self.etimes[i], v, \
                            self.est_tdiffs[i], self.tdiff_errs[i])
        return ostr

    #--------------------------------------------------------------------------
    def load_tdiff(self, tdiff_col, terr_col, tband_col, val_col, stime_cols,
                   etime_cols, time_fmt, split_col=None):
        '''Load a tdiff file.

        Parameters
        -------------
        tdiff_col : (int)
            File column number containing the tdiff estimate (zero offset)
        terr_col : (int)
            File column number containing the tdiff uncertainty (zero offset)
        tband_col : (int)
            File column number containing transmission frequency band
            (zero offset)
        val_col : (int)
            File column number containing validation flag (zero offset)
        stime_cols : (list of int)
            File numbers containing strings that will be formated into start
            times (zero offset)
        etime_cols : (list of int)
            File numbers containing strings that will be formated into end times
            (zero offset)
        time_fmt : (str)
            String to cast starting and ending time strings as a datetime object
        hsplit : (str or NoneType)
            Character seperating data labels in header.  None splits on all
            whitespace characters. (default=None)

        Returns
        ---------
        void : Updates radTdiff object
        '''
        # Test column input
        all_cols = [tdiff_col, terr_col, tband_col]
        all_cols.extend(stime_cols)
        all_cols.extend(etime_cols)
        if min(all_cols) < 0:
            logging.error("Invalid column number [{:}]".format(all_cols))
            return

        max_col = max(all_cols)
        
        # Open the specified file
        f = open(self.tdiff_file, "r")

        if not f:
            logging.error("unable to open file [{:}]".format(self.tdiff_file))
            return

        # Cycle through the file lines
        bad_lines = 0
        for fline in f.readlines():
            # Ignore any header lines
            if fline.find("#") < 0:
                # Split the data into a list
                fdata = fline.split(split_col)

                if len(fdata) <= max_col:
                    bad_lines += 1
                else:
                    # Format and append the starting and ending times
                    try:
                        time_str = str(fdata[stime_cols[0]])
                        for i in range(len(stime_cols) - 1):
                            icol = stime_cols[i+1]
                            time_str = "{:s} {:s}".format(time_str, fdata[icol])
                        self.stimes.append(dt.datetime.strptime(time_str,
                                                                time_fmt))

                        time_str = str(fdata[etime_cols[0]])
                        for i in range(len(etime_cols) - 1):
                            icol = etime_cols[i+1]
                            time_str = "{:s} {:s}".format(time_str, fdata[icol])
                        self.etimes.append(dt.datetime.strptime(time_str,
                                                                time_fmt))
                    except:
                        estr = "Can't format times using format ["
                        estr = "{:s}{:}]".format(estr, time_fmt)
                        logging.warning(estr)
                        bad_lines += 1
                        continue

                    # Cast and append the desired data
                    self.tbands.append(int(fdata[tband_col]))
                    self.est_tdiffs.append(float(fdata[tdiff_col]))
                    self.tdiff_errs.append(float(fdata[terr_col]))
                    self.validated.append(bool(fdata[val_col]))

        # Close the file and exit
        f.close()

        if bad_lines > 0:
            logging.info("{:d} short lines removed".format(bad_lines))

        return

    #--------------------------------------------------------------------------
    def load_hardware_tdiff(self):
        '''Load the hardware tdiff.

        Returns
        ---------
        void : Updates radTdiff object
        '''
        import davitpy.pydarn.radar as pyrad

        # Load the hardware files
        rad_hdw = pyrad.radar(self.rad_code)

        # Load the frequency bands
        rad_tbands = pyrad.tdiff.rad_freqbands.radFreqBands(self.rad_code)

        # Cycle through the hardware entries
        stime = rad_hdw.stTime
        for hard in rad_hdw.sites:
            # The hardware tdiff has no frequency dependence, assign to all
            # frequency bands
            for tt in rad_tbands.tbands:
                self.stimes.append(stime)
                self.etimes.append(hard.tval)
                self.tbands.append(tt)
                self.est_tdiffs.append(hard.tdiff)
                self.tdiff_errs.append(np.nan)
                self.validated.append(True)

            # Move the next start time to the current end time
            stime = hard.tval

        return

    #--------------------------------------------------------------------------
    def get_tdiff(self, tband, ttime, tval=True):
        '''Get tdiff for a specified frequency band and time

        Parameters
        -------------
        tband : (int)
            Transmision frequency band
        ttime : (datetime)
            Time
        tval : (bool)
            Require validated tdiff (default=True)

        Returns
        -----------
        etdiff : (float)
            Estimated tdiff in microsec (np.nan if not available)
        etdiff_err : (float)
            Estimated tdiff uncertainty in microsec (np.nan if not available)
        '''
        etdiff = np.nan
        etdiff_err = np.nan

        #------------------------------------------------
        # Get the desired index
        itbands = np.where(np.array(self.tbands) == tband)[0]

        if len(itbands) > 0:
            itime = np.where(np.array(self.stimes)[itbands] <= ttime)[0]

            if len(itime) > 0:
                idiff = itbands[itime]
                itime = np.where(np.array(self.etimes)[idiff] >= ttime)[0]

                if len(itime) == 1:
                    idiff = itbands[itime]

                    if not tval or (tval and self.validated[idiff]):
                        etdiff = self.est_tdiffs[idiff]
                        etdiff_err = self.tdiff_errs[idiff]

        return etdiff, etdiff_err
