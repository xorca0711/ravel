# Review the unchanged v2 metadata logic while capturing every actual warning.
warning_records <- list()
withCallingHandlers(
  source('Research Article/ungated_navarro_negredo_2026_aged_brain_il10/scripts/qualify_rds_v2.R',local=globalenv()),
  warning=function(w) {
    warning_records[[length(warning_records)+1L]] <<- list(
      message=conditionMessage(w),classes=class(w),call=paste(deparse(conditionCall(w)),collapse=' '))
    invokeRestart('muffleWarning')
  }
)
jsonlite::write_json(list(count=length(warning_records),records=warning_records),
  file.path(commandArgs(trailingOnly=TRUE)[2],'captured_warnings.json'),pretty=TRUE,auto_unbox=TRUE)
