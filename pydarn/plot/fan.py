import pydarn,numpy,math,matplotlib,calendar,datetime,utils,pylab
import matplotlib.pyplot as plot
import matplotlib.lines as lines
from matplotlib.ticker import MultipleLocator
from matplotlib.collections import PolyCollection

def plotFan(dateStr,rad,time=[2,2],interval=60,fileType='fitex',param='velocity', \
scale=[],channel='a',coords='geo',colors='lasse',gsct=0,pdf=0):
	"""
	*******************************
	
	plotFan(dateStr,rad,beam,[time],[fileType]):
	
	crate an rti plot for a secified radar and time period

	INPUTS:
		dateStr: a string containing the target date in yyyymmdd format
		rad: the 3 letter radar code, e.g. 'bks'
		[time]: the range of times for which the file should be read,
			in SIMPLIFIED [hhmm,hhmm] format, eg [29,156], 
			instead of [0029,0156]
			note that an end time of 2400 will read to the end of the file
			default = [0,0]
		[interval]: the interval between fan plots, in seconds
	OUTPUTS:

	EXAMPLE:
		
	Written by AJ 20120905
	*******************************
	"""
	
	
	#check the inputs
	assert(isinstance(dateStr,str) and len(dateStr) == 8),'error, dateStr must be a string 8 chars long'
	#assert(isinstance(rad,str) and len(rad) == 3),'error, dateStr must be a string 3 chars long'
	assert(coords == 'geo'),"error, coords must be one of 'geo'"
	assert(param == 'velocity' or param == 'power' or param == 'width' or \
		param == 'elevation' or param == 'phi0'), \
		"error, allowable params are 'velocity','power','width','elevation','phi0'"
	assert(scale == [] or len(scale)==2), \
	'error, if present, scales must have 2 elements'
	assert(colors == 'lasse' or colors == 'aj'),"error, valid inputs for color are 'lasse' and 'aj'"
	
	if(scale == []):
		if(param == 'velocity'): scale=[-200,200]
		elif(param == 'power'): scale=[0,30]
		elif(param == 'width'): scale=[0,150]
		elif(param == 'elevation'): scale=[0,50]
		elif(param == 'phi0'): scale=[-numpy.pi,numpy.pi]
			
	nTimes = (time[1]-time[0])/interval+1
	if(time[0] == time[1]): time[1] = time[0]+interval/60
	#read the radar data
	
	myData=[]
	for i in range(0,len(rad)):
		data = pydarn.io.radDataRead(dateStr,rad[i],time=time,fileType=fileType,vb=0)
		if(data.nrecs > 0):
			data.getChannel(channel)
			myData.append(data)
	
	#assert(myData.nrecs > 0),'error, no data available'
	
	t1 = datetime.datetime.now()
	for i in range(0,nTimes):
		myFig = plot.figure()
		
		myMap = pydarn.plot.map(limits=None, lon_0=290., hemi='north', boundingLat=None, \
			grid=True, fillContinents='white', fillOceans='white', fillLakes='white', coastLineWidth=.5)
		myMap.drawstates(linewidth=0.5, color='k')
		
		myMap.drawcountries(linewidth=0.5, color='k')
		
		for j in range(0,len(myData)):
			pydarn.plot.overlayRadar(myMap, ids=myData[j][myData[j].times[0]]['prm']['stid'], dateTime=myData[j].times[0], coords=coords)
			pydarn.plot.overlayFov(myMap, ids=myData[j][myData[j].times[0]]['prm']['stid'], dateTime=myData[j].times[0], coords=coords)
			if(myData[j].nrecs > 0):
				plotFanData(myData[j],myFig,myMap,param,scale,coords,colors,gsct)
		
		myFig.show()
		
	print datetime.datetime.now()-t1

def plotFanData(myData,myFig,myMap,param,scale,coords='geo',colors='lasse',gsct=0):
	"""
	*******************************
	
	plotData(myData,myFig,param,scale,bottom,[yrng],[coords],[pos],[colors]):
	
	plots a frequency and Nave panel on Figure myFig at position pos

	INPUTS:
	OUTPUTS:

		
	Written by AJ 20120905
	*******************************
	"""
	site = pydarn.radar.network().getRadarById(myData[myData.times[0]]['prm']['stid']).getSiteByDate(myData.times[0])
	myFov = pydarn.radar.radFov.fov(site=site,rsep=myData[myData.times[0]]['prm']['rsep'],\
	ngates=myData[myData.times[0]]['prm']['nrang']+1,nbeams= site.maxbeam+1)	
	
	verts,intensities,gs_flg = [],[],[]
	
	#collect the data into a list of vertices to be plotted
	for t in myData.times:
		
		#loop through gates with scatter
		for k in range(0,len(myData[t]['fit']['slist'])):
			r = myData[t]['fit']['slist'][k]

			x1,y1 = myMap(myFov.lonCenter[myData[t]['prm']['bmnum']][r],myFov.latCenter[myData[t]['prm']['bmnum']][r])
			x2,y2 = myMap(myFov.lonCenter[myData[t]['prm']['bmnum']][r+1],myFov.latCenter[myData[t]['prm']['bmnum']][r+1])
			x3,y3 = myMap(myFov.lonCenter[myData[t]['prm']['bmnum']+1][r+1],myFov.latCenter[myData[t]['prm']['bmnum']+1][r+1])
			x4,y4 = myMap(myFov.lonCenter[myData[t]['prm']['bmnum']+1][r],myFov.latCenter[myData[t]['prm']['bmnum']+1][r])
			
			#save the polygon vertices
			verts.append(((x1,y1),(x2,y2),(x3,y3),(x4,y4),(x1,y1)))
			#print ((x1,y1),(x2,y2),(x3,y3),(x4,y4))
			#myFig.gca().add_patch(matplotlib.patches.Polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4),(x1,y1)],fill=1,facecolor='red',edgecolor='black'))
			#save the param to use as a color scale
			if(param == 'velocity'): intensities.append(myData[t]['fit']['v'][k])
			elif(param == 'power'): intensities.append(myData[t]['fit']['p_l'][k])
			elif(param == 'width'): intensities.append(myData[t]['fit']['w_l'][k])
			elif(param == 'elevation' and myData[j]['prm']['xcf']): intensities.append(myData[t]['fit']['elv'][k])
			elif(param == 'phi0' and myData[j]['prm']['xcf']): intensities.append(myData[t]['fit']['phi0'][k])
			if(gsct): gs_flg.append(myData[t]['fit']['gflg'][k])

	if(gsct == 0):
		inx = numpy.arange(len(verts))
	else:
		inx = numpy.where(numpy.array(gs_flg)==0)
		x=PolyCollection(numpy.array(verts)[numpy.where(numpy.array(gs_flg)==1)],facecolors='.3',edgecolors='k',linewidths=.3,alpha=.5,zorder=4)
		myFig.gca().add_collection(x, autolim=True)
		
	pcoll = PolyCollection(numpy.array(verts)[inx],edgecolors='k',linewidths=.3,closed=False,zorder=5)
	#set color array to intensities
	pcoll.set_array(numpy.array(intensities)[inx])
	myFig.gca().add_collection(pcoll, autolim=True)

	#myMap.colorbar(mappable=pcoll, location='right', size='5%', pad='2%')
	
	pydarn.plot.plotUtils.genCmap(myMap,pcoll,param,scale,colors=colors,map=1)
