docker build --tag argos-adf .

docker tag argos-adf bams-aws.refinitiv.com:5001/tsbkk-innovation/argos/argos-deploy:argos-adf

docker push bams-aws.refinitiv.com:5001/tsbkk-innovation/argos/argos-deploy:argos-adf
