library("OpenImageR")
library(Thermimage)
library(data.table)

print("start R program")
te<-function(p0,p1,Z){

  reave<-NULL
  for(i in 1:length(p0))
    reave[i]<-format(round(Z[p0[i], p1[i]],digits = 1),nsmall=1)

  return(reave)
}

f<-list()

f<-paste0(system.file("extdata/data/thermo_img/get_heat_source/D (1).jpg", package="Thermimage"))
f<-c(f,paste0(system.file("extdata/data/thermo_img/get_heat_source/D (2).jpg", package="Thermimage")))
f<-c(f,paste0(system.file("extdata/data/thermo_img/get_heat_source/D (3).jpg", package="Thermimage")))
f<-c(f,paste0(system.file("extdata/data/thermo_img/get_heat_source/D (4).jpg", package="Thermimage")))
f<-c(f,paste0(system.file("extdata/data/thermo_img/get_heat_source/D (5).jpg", package="Thermimage")))
f<-c(f,paste0(system.file("extdata/data/thermo_img/get_heat_source/D (6).jpg", package="Thermimage")))
f<-c(f,paste0(system.file("extdata/data/thermo_img/get_heat_source/D (7).jpg", package="Thermimage")))
f<-c(f,paste0(system.file("extdata/data/thermo_img/get_heat_source/D (8).jpg", package="Thermimage")))
f<-c(f,paste0(system.file("extdata/data/thermo_img/get_heat_source/D (9).jpg", package="Thermimage")))



result_csv<-matrix(0,length(point_picnum),5)
colnames(result_csv)<-c("x","y","z","temp","size")



for(i in 1:length(point_picnum)){
  if(point_picnum[i]==0){
    img<-readflirJPG(f[1], exiftoolpath="installed")
  }
  if(point_picnum[i]==1){
    img<-readflirJPG(f[2], exiftoolpath="installed")
  }
  if(point_picnum[i]==2){
    img<-readflirJPG(f[3], exiftoolpath="installed")
  }
  if(point_picnum[i]==3){
    img<-readflirJPG(f[4], exiftoolpath="installed")
  }
  if(point_picnum[i]==4){
    img<-readflirJPG(f[5], exiftoolpath="installed")
  }
  if(point_picnum[i]==5){
    img<-readflirJPG(f[6], exiftoolpath="installed")
  }
  if(point_picnum[i]==6){
    img<-readflirJPG(f[7], exiftoolpath="installed")
  }
  if(point_picnum[i]==7){
    img<-readflirJPG(f[8], exiftoolpath="installed")
  }
  if(point_picnum[i]==8){
    img<-readflirJPG(f[9], exiftoolpath="installed")
  }

  cams<-flirsettings(f, exiftoolpath="installed", camvals="")
  head(cbind(cams$Info), 20)

  ObjectEmissivity<- cams$Info$Emissivity
  dateOriginal<-cams$Dates$DateTimeOriginal
  dateModif<- cams$Dates$FileModificationDateTime
  PlanckR1<- cams$Info$PlanckR1
  PlanckB<- cams$Info$PlanckB
  PlanckF<- cams$Info$PlanckF
  PlanckO<- cams$Info$PlanckO
  PlanckR2<- cams$Info$PlanckR2
  ATA1<- cams$Info$AtmosphericTransAlpha1
  ATA2<- cams$Info$AtmosphericTransAlpha2
  ATB1<- cams$Info$AtmosphericTransBeta1
  ATB2<- cams$Info$AtmosphericTransBeta2
  ATX<- cams$Info$AtmosphericTransX
  OD<- cams$Info$ObjectDistance
  FD<- cams$Info$FocusDistance
  ReflT<- cams$Info$ReflectedApparentTemperature
  AtmosT<- cams$Info$AtmosphericTemperature
  IRWinT<- cams$Info$IRWindowTemperature
  IRWinTran<- cams$Info$IRWindowTransmission
  RH<- cams$Info$RelativeHumidity
  h<- cams$Info$RawThermalImageHeight
  w<- cams$Info$RawThermalImageWidth

  temperature<-raw2temp(img, ObjectEmissivity, OD, ReflT, AtmosT, IRWinT, IRWinTran, RH, PlanckR1, PlanckB, PlanckF, PlanckO, PlanckR2, ATA1, ATA2, ATB1, ATB2, ATX)
  str(temperature)

  result<-te(point_pich[i],point_picw[i],temperature)

  
  result_csv[i,1]<-point_originx[i]
  result_csv[i,2]<-point_originy[i]
  result_csv[i,3]<-point_originz[i]
  result_csv[i,4]<-result
  result_csv[i,5]<-size[i]
  
}

print(result_csv)

#write.csv(3,'result.csv')
result_csv<-data.frame(result_csv)
write.csv(result_csv,"out/result.csv")
