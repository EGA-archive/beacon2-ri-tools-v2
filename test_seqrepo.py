from ga4gh.vrs.dataproxy import create_dataproxy
seqrepo_rest_service_url = "seqrepo+https://services.genomicmedlab.org/seqrepo"
seqrepo_dataproxy = create_dataproxy(uri=seqrepo_rest_service_url)

import os
os.environ["UTA_DB_URL"] = "postgresql://anonymous:anonymous@uta.biocommons.org:5432/uta/uta_20241220"

from ga4gh.vrs.extras.translator import AlleleTranslator
translator = AlleleTranslator(data_proxy=seqrepo_dataproxy)

allele = translator.translate_from("NC_000023.10:g.60020delinsAAC", "hgvs")
heo = allele.model_dump(exclude_none=True)

print('heo')



