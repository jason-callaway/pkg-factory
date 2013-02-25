#!/bin/bash

function rf_exit {

	rm -f $RF_TMPFILE
	exit $1
}
