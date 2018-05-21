import numpy as np 
import pandas as pd 
import os

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect
)

app=Flask(__name__)

metadata_=pd.read_csv('Belly_Button_Biodiversity_Metadata.csv')
otu_=pd.read_csv('belly_button_biodiversity_otu_id.csv')
samples_=pd.read_csv('belly_button_biodiversity_samples.csv')

#Routes
@app.route('/')
def home():
    """Return the dashboard homepage."""
    return render_template('index.html')

@app.route('/names')
def names():
    """List of sample names."""
    all_bact = list(samples_)
    all_bact.pop(0)
    return jsonify(all_bact)

@app.route('/otu')
def otu():
    """List of OTU descriptions."""
    all_otu=list(otu_['lowest_taxonomic_unit_found'])
    return jsonify(all_otu)

@app.route('/metadata/<sample>')
def sampler(sample):
    """MetaData for a given sample."""
    samp={}
    sample_=sample[3:]
    samp['AGE']=int(metadata_[metadata_['SAMPLEID']==int(sample_)]['AGE'])
    samp['BBTYPE']=metadata_[metadata_['SAMPLEID']==int(sample_)]['BBTYPE'].item()
    samp['ETHNICITY']=metadata_[metadata_['SAMPLEID']==int(sample_)]['ETHNICITY'].item()
    samp['GENDER']=metadata_[metadata_['SAMPLEID']==int(sample_)]['GENDER'].item()
    samp['LOCATION']=metadata_[metadata_['SAMPLEID']==int(sample_)]['LOCATION'].item()
    samp['SAMPLEID']=sample_

    return jsonify(samp)


@app.route('/wfreq/<sample>')
def wfreq(sample):
    """Weekly Washing Frequency as a number."""
    samp_={}
    sample_=sample[3:]
    samp_['WFREQ']=metadata_[metadata_['SAMPLEID']==int(sample_)]['WFREQ'].item()

    return jsonify(samp_)

@app.route('/samples/<sample>')
def supersampler(sample):
    """OTU IDs and Sample Values for a given sample."""
    sample_='BB_'+sample[3:]
    a=samples_[samples_[sample_]>0]
    b=a.sort_values(sample_,ascending=False)
    otu_=b['otu_id'].tolist()
    col_=b[sample_].tolist()
    super_={}
    super_['otu_ids']=otu_
    super_['sample_values']=col_
    return jsonify(super_)

if __name__ == "__main__":
    app.run(debug=True)
