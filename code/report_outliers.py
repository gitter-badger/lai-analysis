from __future__ import absolute_import, unicode_literals
import os
import laiutils
from celeryutils import tasks


def main():
    twilio_object = laiutils.TwilioCarriers(os.getenv("TWILIO_SID"),
                                            os.getenv("TWILIO_TOKEN"))
    twilio_object.initialize_carrier_reference("US")
    carrier_reference = twilio_object.carrier_reference
    fp = laiutils.FeedProcessor(carrier_reference)
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_list = [in_file for in_file in
                 laiutils.Utility.get_source_files_from_dir(fp.src_dir)]
    print len(file_list)
    for target_file in file_list:
        tasks.process_feed_file.delay(target_file, carrier_reference,
                                      base_path)
    print("Done!")

if __name__ == "__main__":
    main()
