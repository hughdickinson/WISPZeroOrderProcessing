if __name__ == "__main__" :
    from ZerothOrderWavelengthRanges import ZerothOrderWavelengthRanges
    import pandas as pd
    import sys

    # hardcoded values
    expectedArgNumber = 5
    requiredArgumentNames = [
    'stampPath',
    'datFileInputPath',
    'datFileOutputPath',
    'regionFilePath',
    'cataloguePath'
    ]
    requiredArgumentDescriptions = [
    'Path to the drizzled stamp file.',
    'Path to the input .dat file containing the spectrum wavelengths in the "wave" column.',
    'Path to which a copy of the input .dat file with the "zeroth" column values updated to reflect potential zeroth order contamination should be written.',
    'Path to a SAO DS9 format region file describing the positions of the zeroth order dispersion images in the raw grism image that is appropriate for the drizzled stamp file.',
    'Path to the source catalogue file for the appropriate field that was generated from the appropriate direct image by the sextractor utility.'
    ]
    outputColumnWidth = 15

    # Process script arguments
    if len(sys.argv) < expectedArgNumber :
        print('Error! {0} requires {1} arguments.\n\n{2}\n\n'.format(sys.argv[0],
        expectedArgNumber,
        '\n'.join([ str(argNum + 1) + ')  ' + nameAndDescription[0] + ' -- ' + nameAndDescription[1] for argNum, nameAndDescription in enumerate(zip(requiredArgumentNames, requiredArgumentDescriptions))])))

    stampPath = sys.argv[1]# if len(sys.argv) > 1 else '/Volumes/ramon2_wisps/data/V5.0/Par369/G102_DRIZZLE/aXeWFC3_G102_mef_ID2.fits'
    datFileInputPath = sys.argv[2]# if len(sys.argv) > 2 else '/Volumes/ramon2_wisps/data/V5.0/Par369/Spectra/Par369_G102_BEAM_2A.dat'
    datFileOutputPath = sys.argv[3]# if len(sys.argv) > 3 else 'testDatOut.dat'
    regionFilePath = sys.argv[4]# if len(sys.argv) > 4 else '/Volumes/ramon2_wisps/data/V5.0/Par369/DATA/DIRECT_GRISM/Par369_G102_VM.reg'
    cataloguePath = sys.argv[5]# if len(sys.argv) > 5 else '/Volumes/ramon2_wisps/data/V5.0/Par369/DATA/DIRECT_GRISM/fin_F110.cat'

    # Parse the .dat file into a pandas dataframe
    datFile = open(datFileInputPath)
    columnNames = datFile.readline().split()[1:]
    datFile.close()
    datFileFrame = pd.read_csv(datFileInputPath, delim_whitespace=True, header=0, engine='c', names=columnNames, comment='#')

    # instantiate the class to compute the wavelength ranges affected by zeroth order images
    zeroOrderRanges = ZerothOrderWavelengthRanges(stampPath, regionFilePath, cataloguePath)
    # update the dataframe column for the zeroth orders to reflect the computation
    datFileFrame['zeroth'] = zeroOrderRanges.getWavelengthZerothOrderFlags(datFileFrame['wave'].values)

    # generate some appropriately formatted output
    datFileOutput = '{0}{1}\n'.format('#'.ljust((outputColumnWidth - 1) - len(columnNames[0])), datFileFrame.to_string(col_space=15, index=False, header=True, justify='right', float_format='%10.6f'))

    # write the output to the specified output file.
    outFile = open(datFileOutputPath, 'w')
    outFile.write(datFileOutput)
    outFile.close()

    print('Updated .dat file written to {0}'.format(datFileOutputPath))
