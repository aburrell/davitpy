#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# rad_freqbands.py, Angeline G. Burrell (AGB), UoL
#
# Comments: Routines to define and retrieve frequency bands for the SuperDARN
#           radars.  These would be better saved and accessed through a table,
#           so as to allow for temporal updates.
#-----------------------------------------------------------------------------
'''Define and retrieve transmission frequency bands for the SuperDARN radars.

Parameters
----------------------------------------------------------------------------
rad_band_num : (dict)
rad_min : (dict)
rad_max : (dict)
id_to_code : (dict)
---------------------------------------------------------------------------

Classes
----------------------------------------------------------------------------
radFreqBands
----------------------------------------------------------------------------

Moduleauthor
------------
Angeline G. Burrell (AGB), 25 July 2016, University of Leicester (UoL)
'''
import logging
import datetime as dt
import numpy as np

# Define the frequency bands for different radars
#
# The radar band numbers allow new frequency bands to be added in numerical
# order whilst maintaining backward compatibility.  The bands used will also
# change over time, necessitating time limits (just like hardware files)
rad_band_time = {
    'gbr':{0:[dt.datetime(1995,1,1), dt.datetime(3000,1,1)]},
    'hal':{0:[dt.datetime(1995,1,1), dt.datetime(3000,1,1)]},
    'han':{0:[dt.datetime(1995,1,1), dt.datetime(3000,1,1)]},
    'kap':{0:[dt.datetime(1995,1,1), dt.datetime(3000,1,1)]},
    'kod':{0:[dt.datetime(1995,1,1), dt.datetime(2009,10,1)],
           1:[dt.datetime(2010,8,30), dt.datetime(2010,9,6,23,59,59)],
           2:[dt.datetime(2010,9,7), dt.datetime(3000,1,1)]},
    'ksr':{0:[dt.datetime(1995,1,1), dt.datetime(2004,10,1)],
           1:[dt.datetime(2007,8,30), dt.datetime(3000,1,1)]},
    'pgr':{0:[dt.datetime(1995,1,1), dt.datetime(2001,10,2)],
           1:[dt.datetime(2004,8,30), dt.datetime(2004,10,1)],
           2:[dt.datetime(2007,8,30), dt.datetime(2007,10,1)],
           3:[dt.datetime(2009,8,30), dt.datetime(3000,1,1)]},
    'pyk':{0:[dt.datetime(1995,1,1), dt.datetime(3000,1,1)]},
    'sas':{0:[dt.datetime(1995,1,1), dt.datetime(3000,1,1)]},
    'sto':{0:[dt.datetime(1995,1,1), dt.datetime(3000,1,1)]},
    }
rad_band_num = {
#    'ade':[0,1,2,3,4,5,6,7,8],
#    'adw':[0,1,2,3,4,5,6,7,8],
#    'bks':[0],
#    'cly':[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,
#           25,26],
    'gbr':{0:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,
              25]},
    'hal':{0:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,
            25,26,27,28,29,30,31,32,33,34]},
    'han':{0:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]},
#    'inv': [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,
#            25,26,27],
    'kap':{0:[37,38,39,40,11,12,13,14,15,16,17,18,19,20,21,22,23,24,
              25,26,27,28,29]},
    'kod':{0:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,
              25,26],
           1:[27,28,29,30,31,32,33,34,35,36,37,38,39,12,13,14,15,16,17,18,19,20,
              21,22,23,24,25,26],
           2:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,
              25,26],},
    'ksr':{0:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,41,42,43,22,44,45,26,
              27,46,47,48,32,33,34,35,36],
           1:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,
              25,26,27,28,29,30,31,32,33,34,35,36]},
#    'mcm': [0,1,2,3,4,5,6,7,8],
    'pgr':{0:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,
              25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40],
           1:[0,1,2,3,4,5,41,42,43,9,10,11,12,44,45,46,47,48,49,50,21,22,51,52,
              53,54,28,29,30,31,32,33,34,35,36,37,38,39,40],
           2:[0,1,2,3,4,5,55,56,57,58,59,60,61,44,45,46,47,62,63,64,65,66,22,51,
              52,53,54,28,29,30,31,32,33,34,35,36,37,38,39,40],
           3:[0,1,2,3,4,5,41,42,43,9,10,67,68,61,44,45,46,47,62,63,21,22,51,52,
              53,54,28,29,30,31,32,33,34,35,36,37,38,39,40]},
    'pyk':{0:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]},
#    'rkn': [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,
#            25,26,27],
    'sas':{0:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,
              25,26,27,28,29,30,31]},
    'sto':{0:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]},}

# Radar frequencies saved in kHz
rad_min = {
#    'ade':[10400, 10900, 12000, 13000, 14500, 15000, 16000, 17000, 18000],
#    'adw':[10400, 10900, 12000, 13000, 14500, 15000, 16000, 17000, 18000],
#    'bks':[10210],
#    'cly':[8000, 8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000, 12500,
#           13000, 13469, 13929, 14500, 15040, 15500, 16000, 16500, 17000, 17500,
#           18000, 18500, 19000, 19500, 20040, 20500],
    'gbr':np.array([8900, 9201, 9500, 9966, 10199, 10698, 10900, 11199, 11696,
                    11900, 12201, 12501, 12801, 13291, 13592, 13989, 14199,
                    14500, 15040, 15400, 15840, 16141, 16399, 16900, 17400,
                    17871]),
    'hal':np.array([8000, 8350, 8700, 9000, 9350, 9700, 10000, 10350, 10700,
                    11000, 11350, 11651, 12000, 12300, 12650, 13000, 13350,
                    13700, 14000, 14350, 14651, 15000, 15350, 15651, 16000,
                    16350, 16700, 17000, 17350, 17700, 18000, 18350, 18700,
                    19000, 19350, 19700]),
    'han':np.array([8305, 8965, 9900, 11075, 11550, 12370, 13200, 15010, 16210,
                    16555, 17970, 18850, 19415, 19705, 19800]),
#    'inv':[8000, 8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000, 12500,
#           13000,  13500, 14000, 14500, 15000, 15500, 16000, 16500, 17000,
#           17500, 18000, 18500, 19000,19500,20000,20500,21000,21500],
    'kap':np.array([8900, 9201, 9600, 9966, 10200, 10501, 10701, 11000, 11430,
                    11800, 12100, 12400, 12700, 13000, 13301, 13551, 13971,
                    14380, 14701, 15100, 15400, 15840, 16141, 16399, 16900,
                    17400, 17871, 18000, 18350, 18700]),
    'kod':np.array([8200, 8700, 9200, 9700, 10200, 10701, 11300, 11800, 12300,
                    12800, 13300, 13800, 14500, 15000, 15500, 16100, 16600,
                    17100, 17600, 18100, 18600, 19100, 19600, 20100, 20600,
                    21100, 21600, 8000, 8500, 9000, 9500, 10000, 10500, 11000,
                    11500, 12000, 12500, 13000, 13500, 14000]),
    'ksr':np.array([8000, 8400, 8700, 9000, 9300, 9600, 9900, 10200, 10500,
                    10800, 11100, 11400, 11700, 12000, 12300, 12600, 12900,
                    13400, 13700, 14100, 14500, 14800, 15000, 15300, 15700,
                    16000, 16400, 16900, 17400, 17900, 18400, 18900, 19400, 
                    19900, 20400, 20900, 21400, 8000, 9000, 10000, 11000,
                    13700, 14001, 14300, 15300, 15600, 17400, 18100, 18800]),
#    'mcm':[10100, 10700, 11400, 12500, 13700, 14400, 15200, 17000, 18400],
    'pgr':np.array([8016, 8317, 8618, 9000, 9301, 9487, 9901, 10200, 10501,
                    10900, 11000, 11300, 11700, 12001, 12995, 13100, 13500,
                    13801, 14101, 14500, 14800, 15101, 15500, 15900, 16200,
                    16501, 16900, 17200, 17500, 17800, 18000, 18301, 18701,
                    19000, 19300, 19600, 19900, 20200, 20500, 20800, 21100,
                    9901, 10300, 10601, 12001, 12995, 13300, 13600, 14000,
                    14301, 14600, 15900, 16300, 16701, 17000, 9901, 10000,
                    10400, 10800, 11000, 11400, 11800, 14000, 14400, 14700,
                    15000, 15400, 11100, 11500]),
    'pyk':np.array([8000, 8430, 8985, 10155, 10656, 11290, 11475, 12105, 12305,
                    12590, 13360, 13875, 14400, 15805, 16500, 16820, 18175,
                    18835, 19910]),
#    'rkn':[8000, 8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000, 12500,
#           13000,  13419, 14000, 14500, 15000, 15500, 16000, 16500, 17000,
#           17500, 18000, 18500, 19000,19500,20000,20500,21000,21500],
    'sas':np.array([8000, 8907, 9208, 9600, 10100, 10499, 11000, 11300, 11600,
                    12300, 12995, 13416, 13800, 14100, 14400, 14701, 15002,
                    15390, 15801, 16100, 16400, 16701, 17000, 17300, 17600,
                    17900, 18200, 18500, 18800, 19100, 19400, 19700]),
    'sto':np.array([8202, 8900, 9200, 9501, 10000, 11100, 11401, 11800, 12301,
                    12801, 13100, 13501, 13901, 14400, 14901, 16100, 16689,
                    16799, 17910, 18778, 19674]),
}

rad_max = {
#    'ade':[10700, 11200, 12300, 13300, 14800, 15300, 16300, 17300, 18300],
#    'adw':[10700, 11200, 12300, 13300, 14800, 15300, 16300, 17300, 18300],
#    'bks':[10710],
#    'cly':[8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000, 12500, 13000,
#           13469, 13929, 14500, 15040, 15500, 16000, 16500, 17000, 17500,
#           18000, 18500, 19000, 19500, 20040, 20500, 21000],
    'gbr':np.array([9200, 9499, 9965, 10198, 10697, 10899, 11198, 11695, 11899,
                    12200, 12500, 12800, 13290, 13591, 13988, 14198, 14499,
                    14960, 15399,15700, 16140, 16398, 16899,17399, 17870,
                    18000]),
    'hal':np.array([8349, 8699, 8999, 9249, 9699, 9999, 10349, 10699, 10999,
                    11349, 11650, 11999, 12299, 12949, 12999, 13349, 13699,
                    13999, 14349, 14650, 14999, 15349, 15650, 15999, 16349,
                    16699, 16999, 17349, 17699, 17999, 18349, 18699, 18999,
                    19349, 20000]),
    'han':np.array([8335, 9040, 9985, 11275, 11600, 12415, 13260, 15080, 16360,
                    16615, 18050, 18865, 19680, 19755, 19990]),
#    'inv':[8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000, 12500,
#           13000,  13500, 14000, 14500, 15000, 15500, 16000, 16500, 17000,
#           17500, 18000, 18500, 19000,19500,20000,20500,21000,21500,22000],
#    'mcm':[10400, 11000, 11700, 12800, 14000, 14700, 15500, 17300, 18700],
    'kap':np.array([9200, 9599, 9965, 10199, 10500, 10700, 10999, 11429, 11799,
                    12099, 12399, 12699, 12999, 13300, 13550, 13970, 14379,
                    14700, 15099, 15399, 15700, 16140, 16398, 16899, 17399,
                    17870, 17999, 18349,18699, 19000]),
    'kod':np.array([8699, 9199, 9699, 10199, 10700, 11299, 11799, 12299, 12799,
                    13299, 13799, 14499, 14999, 15499, 16099, 16599, 17099,
                    17599, 18099, 18599, 19099, 19599, 20099, 20599, 21099,
                    21599, 22100, 8499, 8999, 9499, 9999, 10499, 10999, 11499,
                    11999, 12499, 12999, 13499, 13999, 14499]),
    'ksr':np.array([8399, 8699, 8999, 9299, 9599, 9899, 10199, 10499, 10799,
                    11099, 11399, 11699, 11999, 12299, 12599, 12899, 13399,
                    13699, 14099, 14499, 14799, 14999, 15299, 15699, 15999,
                    16399, 16899, 17399, 17899, 18399, 18899, 19399, 19899,
                    20399, 20899, 21399, 21900, 8999, 9999, 10999, 11399,
                    14000, 14299, 14999, 15599, 16399, 18099, 18799, 19399]),
    'pgr':np.array([8316, 8617, 8999, 9300, 9486, 9900, 10199, 10500, 10899,
                    10999, 11299, 11699, 12000, 12994, 13099, 13499, 13800,
                    14100, 14499, 14799, 15100, 15499, 15899, 16199, 16500,
                    16899, 17199, 17499, 17799, 17999, 18300, 18700, 18999,
                    19299, 19599, 19899, 20199, 20499, 20799, 21099, 21300,
                    10299, 10600, 10899, 12996, 13299, 13599, 13999, 14300,
                    14599, 15100, 16299, 16700, 16999, 17499, 9999, 10399,
                    10799, 10999, 11399, 11799, 12000, 14399, 14699, 14999,
                    15399, 11499, 11799]),
    'pyk':np.array([8195, 8850, 9395, 10655, 11175, 11450, 11595, 12235, 12510,
                    13280,13565, 13995, 15015, 16365, 16685, 17475, 18770,
                    18885, 20000]),
#    'rkn':[8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000, 12500,
#           13000,  13419, 14000, 14500, 15000, 15500, 16000, 16500, 17000,
#           17500, 18000, 18500, 19000,19500,20000,20500,21000,21500,22000],
    'sas':np.array([8300, 9207, 9599, 9900, 10498, 10999, 11299, 11599, 12000,
                    12600, 13355, 13799, 14099, 14399, 14700, 15001, 15389,
                    15800, 16099, 16399, 16700, 16999, 17299, 17599, 17899,
                    18199, 18499, 18799, 19099, 19399, 19699, 19985]),
    'sto':np.array([8500, 9199, 9500, 9900, 10300, 11400, 11799, 12300, 12800,
                    13099, 13500, 13900, 14399, 14900, 15400, 16455, 16748,
                    16815, 17990, 18905, 19686]),}

# Allow use of both 3-letter code and numerical IDs
id_to_code = {1:'gbr', 2:'sch', 3:'kap', 4:'hal', 5:'sas', 6:'pgr', 7:'kod',
              8:'sto', 9:'pyk', 10:'han', 11:'san', 12:'sys', 13:'sye',
              14:'tig', 15:'ker', 16:'ksr', 18:'unw', 20:'mcm', 21:'fir',
              32:'wal', 33:'bks', 40:'hok', 64:'inv', 65:'rkn', 90:'lyr',
              128:'spe', 209:'ade', 208:'adw',}

#-----------------------------------------------------------------------------
class radFreqBands(object):
    '''Contains the transmission frequency bands for a given radar

    Parameters
    ------------
    rad : (str or int)
       3-character radar code or numerical ID number
    rtime : (datetime)
       datetime object with date to retrieve radar bands (default=today)

    Attributes
    ------------
    rad_code : (str)
        Radar 3-character code (lowercase only)
    stid : (int)
        Radar numerical ID
    stime : (datetime)
        Time radar bands became valid
    etime : (datetime)
        Time radar bands are no longer valid
    tbands : (list)
        Transmision frequency band numbers
    tmins : (np.array)
        Array of transmission frequency band lower boundaries (kHz)
    tmaxs : (np.array)
        Array of transmission frequency band upper boundaries (kHz)

    Methods
    ---------
    get_tband_max_min
    get_mean_tband_freq
    get_tfreq_band_num

    written by AGB 25/07/16
    '''
    def __init__(self, rad=None, rtime=dt.datetime.today()):

        # Assign the radar IDs
        if id_to_code.has_key(rad):
            self.rad_code = id_to_code[rad]
            self.stid = rad
        else:
            self.rad_code = rad
            self.stid = None

            if rad is not None:
                for stid in id_to_code.keys():
                    if id_to_code[stid] == rad.lower():
                        self.stid = stid
                        break
                    
        # Assign the frequency bands
        try:
            tkey = self.get_time_key(rtime)
            self.stime = rad_band_time[self.rad_code][tkey][0]
            self.etime = rad_band_time[self.rad_code][tkey][1]
            self.tbands = rad_band_num[self.rad_code][tkey]
            self.tmins = rad_min[self.rad_code][self.tbands]
            self.tmaxs = rad_max[self.rad_code][self.tbands]
        except:
            self.stime = rtime
            self.etime = rtime
            self.tbands = list()
            self.tmins = np.empty(shape=0)
            self.tmaxs = np.empty(shape=0)

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
        In[1]: fb = davitpy.pydarn.radar.tdiff.rad_freqbands.radFreqBands(10)
        In[2]: print fb
        Radar transmission frequency bands:
            Code: han       ID: 10
            Valid between: 1995-01-01 00:00:00 and 3000-01-01 00:00:00
            Number of frequency bands spanning 8.305-19.990 MHz: 15
                Band Min_Freq-Max_Freq (MHz)
                00 8.305-8.335
                01 8.965-9.040
                02 9.900-9.985
                03 11.075-11.275
                04 11.550-11.600
                05 12.370-12.415
                06 13.200-13.260
                07 15.010-15.080
                08 16.210-16.360
                09 16.555-16.615
                10 17.970-18.050
                11 18.850-18.865
                12 19.415-19.680
                13 19.705-19.755
                14 19.800-19.990
        '''
        ostr = "Radar transmission frequency bands:\n"
        # Add radar name
        ostr = "{:s}\tCode: {:}\tID: {:}\n".format(ostr, self.rad_code,
                                                   self.stid)
        ostr = "{:s}\tValid between: {:} and {:}\n".format(ostr, self.stime,
                                                           self.etime)
        # Add number of frequency bands
        if len(self.tbands) == 0:
            ostr = "{:s}\tNo frequency bands".format(ostr)
        else:
            ostr = "{:s}\tNumber of frequency bands spanning ".format(ostr)
            ostr = "{:s}{:.3f}-{:.3f} ".format(ostr, min(self.tmins) * 1.0e-3,
                                               1.0e-3 * max(self.tmaxs))
            ostr = "{:s}MHz: {:d}\n".format(ostr, len(self.tbands))
            # Add the frequency bands
            ostr = "{:s}\t\tBand Min_Freq-Max_Freq (MHz)\n".format(ostr)
            for i,mm in enumerate(self.tmins):
                ostr = "{:s}\t\t{:02d} {:.3f}-{:.3f}\n".format(ostr,
                                                               self.tbands[i],
                                                               mm * 1.0e-3,
                                                               1.0e-3 *
                                                               self.tmaxs[i])
        return ostr

    #--------------------------------------------------------------------------
    def get_time_key(self, rtime):
        '''Return the time key for the radar frequency bands

        Parameters
        -----------
        ttime : (datetime)
            Time to retrieve

        Returns
        ---------
        tval : (int)
            Key or -1 if no valid time ranges are found
        '''
        
        for tkey in rad_band_time[self.rad_code].keys():
            time_limits = rad_band_time[self.rad_code][tkey]
            if(time_limits[0] <= rtime and time_limits[1] > rtime):
                return tkey

        return -1
    
    #--------------------------------------------------------------------------
    def get_tband_max_min(self, tfreq):
        '''Return the maximum and minimum frequency for the band that the
        supplied frequency falls into

        Parameters
        -------------
        tfreq : (int)
            Transmision frequency in kHz

        Returns
        -----------
        min_freq : (int)
            Minimum frequency in kHz, -1 if unavailable
        max_freq : (int)
            Maximum frequency in kHz, -1 if unavailable
        '''
        #------------------------------------------------
        # Cycle through the transmission frequency bands
        for i,t in enumerate(self.tmins):
            if tfreq - t >= 0 and self.tmaxs[i] - tfreq >= 0:
                return(t, self.tmaxs[i])
        
        logging.warn("Unknown transmission freq [{:d} kHz]".format(tfreq))
        return(-1, -1)

    def get_mean_tband_freq(self, tband):
        ''' Return the maximum and minimum frequency for the band that the
        supplied frequency falls into

        Parameters
        -------------
        tband : (int)
            Transmision band number

        Returns
        -----------
        mean_freq : (int)
            Mean frequency in kHz, -1 if unavailable
        '''
        mean_freq = -1
            
        #--------------------------------------------
        # Ensure that band information is available
        if len(self.tmins) > tband:
            mean_freq = int((self.tmaxs[tband] + self.tmins[tband])
                            / 2.0)
        else:
            estr = "unknown transmission freq band [{:}]".format(tband)
            logging.warn(estr)

        return mean_freq

    def get_tfreq_band_num(self, tfreq):
        ''' Retrieve the transmision frequency band number for a specified
        frequency

        Parameters
        -----------
        tfreq : (int)
            Transmission frequency in kHz

        Returns
        ---------
        tband : (int)
            Transmission frequency band number, -1 if unavailable
        '''
        #--------------------------------------------
        # Cycle through the different frequency bands
        for i,t in enumerate(self.tmins):
            if t <= tfreq and tfreq <= self.tmaxs[i]:
                return(self.tbands[i])
        
        logging.warn("no band for frequency [{:} kHz]".format(tfreq))
        return(-1)
