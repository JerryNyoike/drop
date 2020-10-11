from . import db
from subprocess import Popen
from asyncio import create_task
from os import path, makedirs, remove
from datetime import datetime
from .helpers import log_error


async def get_metadata(beat_file):
	'''
	This function gets the metadata from the media file 
	passed as beat_file and saves it to the database.
	'''
	output_file = ".\\instance\\temp\\{}_{}.txt".format(datetime.now().strftime("%d%m%Y%H%M%S"), beat_file.split("\\")[-1].split(".")[0])
	argv = [
		beat_file,
		"ffmetadata",
		output_file
	]

	try:
		p = Popen(["ffmpeg", "-i", argv[0], "-f", argv[1], argv[2]])
		p.communicate()
		# with open(output_file, "r") as f:
		# 	metadata = dict()
		# 	for line in f.read().split("\n"):
		# 		pair = line.split("=")
		# 		if len(pair) > 1:
		# 			metadata[pair[0]] = pair[1]

	except OSError as e:
		log_error("At get_metadata, " + str(e), "os_error_logs.txt")

	

async def main(beat_file):

	# Schedule the get metadata function execution
	await create_task(get_metadata(beat_file))