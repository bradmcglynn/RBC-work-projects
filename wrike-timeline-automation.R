#STEP ONE: set working directory to source file location

 

#string of plan name

plan_name <- readline("Enter Plan Acronym: ")

 

#Read, Write and Edit xlsx Files

library(openxlsx)

#tools for cleaning and combining data, particularly w/ grouped and time series data

library(DataCombine)

#practical numerical math functions - uses some MATLAB fcn names to simplify porting

library(pracma)

#non tabular data manipulation - work w/ list objects

library(rlist)

#tools to parse and maniplulate dates

library(lubridate)

 

#edit implementation timeline, turn to csv, then import here

#skip = 1 - no skipping blank lines

raw<-read.csv("Import.csv",header=T,skip=1)[,1:8]

 

 

#turn N/A values to blanks

raw[is.na(raw)]<-""

 

#EDIT: CONVERT DATES FROM FACTORS TO DATE

raw$Start.Date <- as.Date(ymd(raw$Start.Date))

raw$Finish.Date <- as.Date(ymd(raw$Finish.Date))

# raw$Start.Date <- format(as.Date(raw$Start.Date, format = "%d/%m/%Y"), "%Y/%m/%d")

# raw$Finish.Date <- format(as.Date(raw$Finish.Date, format = "%d/%m/%Y"), "%Y/%m/%d")

 

#generate strings of Responsible

responsible<-as.character(raw$Responsible)

 

#ASSIGNING A UNIQUE NUMBER TO EACH CATEGORY

#first row is 0 (empty), second row is labelled 1

ifolderindex<-c(0,1)

 

for (a in 3:nrow(raw)){

  #if a row in Category (type of work) IS empty: add a "O" to ifolderindex

  if (raw$Category[a] == ""){

    ifolderindex<-append(ifolderindex,0)

  }

  #if Category NOT empty:

  else {

    #if Category not equal to one above it, add 1 to the label of row 2 above it

    #it's a-2 in case row above is a blank

    if (raw$Category[a] != raw$Category[(a-1)]){

      ifolderindex<-append(ifolderindex,(ifolderindex[a-2])+1)

      #if it is equal to the one above it, label it the same number

    }else {

      ifolderindex<-append(ifolderindex,(ifolderindex[a-1]))

    }

  }

}

 

ikey<-c(); ifolder<-c(); iparent_tasks<-c(); ititle<-c(); iworkflow<-c()

istatus<-c(); icustom_status<-c(); ipriority<-c(); iassign<-c(); istart<-c()

iduration<-c(); iduration_hours<-c(); itime_spent<-c(); iend<-c(); idepends<-c()

istart_date_constraint<-c(); idescription<-c(); iallocated_hour<-c()

 

 

for (j in 1:nrow(raw)){

  #ikey assigns a # for each row starting from 1; will populate 'Key' column in final doc

  ikey<-append(ikey,j)

  iparent_tasks<-append(iparent_tasks,"")

 

  #appending start and end date of tasks

  istart<-append(istart,raw$Start.Date[j])

  iend<-append(iend,raw$Finish.Date[j])

 

  iduration<-append(iduration,"")

  iduration_hours<-append(iduration_hours,"")

  itime_spent<-append(itime_spent,"")

  istart_date_constraint<-append(istart_date_constraint,"")

  iallocated_hour<-append(iallocated_hour,"")

 

  #if Category row is blank, all vectors below append a blank or /

  if (raw$Category[j]==""){

    istatus<-append(istatus,"")

    icustom_status<-append(icustom_status,"")

    ipriority<-append(ipriority,"")

    iworkflow<-append(iworkflow,"")

    ifolder<-append(ifolder,"/")

    iassign<-append(iassign,"")

    idescription<-append(idescription,"")

  }

 

  #if Category row is NOT blank:

  else{

    #Populates cols 'Workflow' and 'Priority' w/ below statements for every non-blank row

    iworkflow<-append(iworkflow,"Default Workflow")

    ipriority<-append(ipriority,"Normal")

   

    ###

    #IF STATEMENT FOR EACH CATEGORY TYPE

    if (raw$Category[j]=="Client WIN"){

      ifolder<-append(ifolder,paste("/",plan_name," - ",ifolderindex[j]," - ","Client WIN/",sep = ""))

    }

   

    else if (raw$Category[j]=="Data"){

      ifolder<-append(ifolder,paste("/",plan_name," - ",ifolderindex[j]," - ","Data Gathering/",sep = ""))

    }

   

    else if (raw$Category[j]=="Correspondence"){

      ifolder<-append(ifolder,paste("/",plan_name," - ",ifolderindex[j]," - ","Correspondence/", sep = ""))

    }

   

    else if (raw$Category[j]=="Administration"){

      ifolder<-append(ifolder,paste("/",plan_name," - ",ifolderindex[j]," - ","Administration/", sep = ""))

    }

   

    else if (raw$Category[j]=="BuyIn Payroll"){

      ifolder<-append(ifolder,paste("/",plan_name," - ",ifolderindex[j]," - ","Set Up/", sep = ""))

    }

   

    else if (raw$Category[j]=="Tax File"){

      ifolder<-append(ifolder,paste("/",plan_name," - ",ifolderindex[j]," - ","Tax File/", sep = ""))

    }

   

    else if (raw$Category[j]=="Welcome Letter"){

      ifolder<-append(ifolder,paste("/",plan_name," - ",ifolderindex[j]," - ","Welcome Letter/", sep = ""))

    }

    

    else if (raw$Category[j]=="Payroll"){

      ifolder<-append(ifolder,paste("/",plan_name," - ",ifolderindex[j]," - ","Payroll Activities/", sep = ""))

    }

    ###

   

    ###POPULATING 'STATUS' AND CUSTOM STATUS' COLUMNS

    if (tolower(raw$Comments[j])=="done"||tolower(raw$Comments[j])=="completed"){

      idescription<-append(idescription,"")

      istatus<-append(istatus,"Completed")

      icustom_status<-append(icustom_status,"Completed")

    }else {

      idescription<-append(idescription,responsible[j])

      istatus<-append(istatus,"Active")

      icustom_status<-append(icustom_status,"New")

    }

  }

  ###

 

  # || = or

  ###POPULATING 'ASSIGNED TO' COLUMN

  #if already marked as done, no assigning ppl to task

  if (tolower(raw$Comments[j])=="done"||raw$Comments[j]=="Completed"){

    iassign<-append(iassign,"")

  }

 

  #if NOT marked as done:

  else {

    #otherwise assigning ppl based on their team

    #NOTE FOR POSSIBLE FUTURE CHANGES:

   

    if (raw$Responsible[j]=="RBCI"||raw$Responsible[j]=="FINANCE"||raw$Responsible[j]=="B2B Team"||raw$Responsible[j]== " B2B Team"){

      iassign<-append(iassign,"name_list")

    }

    else if (raw$Responsible[j]=="HRSC"||raw$Responsible[j]=="HRCC"||raw$Responsible[j]=="Conduent"||raw$Responsible[j]=="GA"||raw$Responsible[j]=="GBS"){

      iassign<-append(iassign,"name_list")

    }

    else if (raw$Responsible[j]=="RBC I&TS"){

      iassign<-append(iassign,"name_list")

    }

    else if (raw$Responsible[j]=="BUCK"||raw$Responsible[j]=="NOVITEX"||raw$Responsible[j]=="MAILROOM"){

      iassign<-append(iassign,"name_list")

    }

  }

 

  #if Responsible row blank, Add title to row (ex. //AMLPC1 - 1 - Client WIN/)

  if (raw$Responsible[j]==""){

    ititle<-append(ititle,ifolder[j+1])

  }

  #otherwise add step number to task titles

  else {

    ititle<-append(ititle,paste(raw$Task..[j],".",raw$Description[j]))

  }

 

  #adding type of dependencies

  if (raw$Dependencies[j]==""){

    idepends<-append(idepends,"")

  }else{

    idepends<-append(idepends,paste(which(raw$Task.. == raw$Dependencies[j]),"FS"))

  }

}

 

 

#PUTTING TOGETHER ALL THE VECTORS CREATED ABOVE

wrike_import <- data.frame(ikey,ifolder,iparent_tasks,ititle,iworkflow,istatus,icustom_status,ipriority,iassign,istart,iduration,iduration_hours,itime_spent,iend,idepends,istart_date_constraint,idescription,iallocated_hour)

 

#ADDING COLUMN NAMES

colnames(wrike_import)<-c("Key",         "Folder",            "Parent task",              "Title",  "Workflow",      "Status",             "Custom status", "Priority",              "Assigned To",  "Start Date",      "Duration",        "Duration (Hours)",              "Time Spent (Hours)", "End Date",          "Depends On", "Start Date Constraint",       "Description",   "Allocated hours")

 

#WRITE TO CSV FILE

write.csv(wrike_import,"R Export.csv")
