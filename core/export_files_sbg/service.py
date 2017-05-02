# -*- coding: utf-8 -*-
from core import sbg_utils, utils
import boto3

s3 = boto3.resource('s3')


def handler(event, context):
    '''
    export output files from sbg to our s3
    '''

    # get data
    sbg = sbg_utils.create_sbg_workflow(**event.get('workflow'))
    run_response = event.get('run_response')
    ff_meta = event.get('ff_meta')
    uuid = ff_meta['uuid']
    pf_meta = event.get('pf_meta')

    sbg.export_all_output_files(run_response, ff_meta, base_dir=uuid)
    # creating after we export will add output file info to ff_meta
    ff_meta = sbg_utils.create_ffmeta(sbg, **event.get('ff_meta'))
    ff_meta.run_status = "output_files_transferring"

    # create processed file metadata here, because
    # 1) we want to keep track of the uploading status and
    # 2) we want to specify directory and file name before we export
    # (these files can be large so don't change file name after the export which is equivalent to rewriting)
    # pf_meta = sbg_utils.create_processed_file_metadata("uploading", sbg, ff_meta)

    return {'workflow': sbg.as_dict(),
            'ff_meta': ff_meta.as_dict(),
            # 'pf_meta': [pf.as_dict() for pf in pf_meta]
            'pf_meta': pf_meta
            }
