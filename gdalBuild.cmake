cmake .. -DCMAKE_BUILD_TYPE=Release -Donnxruntime_ENABLE_PYTHON=ON -DPYTHON_EXECUTABLE=/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -Donnxruntime_BUILD_SHARED_LIB=ON -Donnxruntime_DEV_MODE=OFF -DPYTHON_INCLUDE_DIR=/Library/Frameworks/Python.framework/Versions/3.11/include/python3.11;/Library/Frameworks/Python.framework/Versions/3.11/include/python3.11 -DNUMPY_INCLUDE_DIR=/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/numpy/core/include/numpy -DPostgreSQL_INCLUDE_DIR=/Applications/Postgres.app/Contents/Versions/15/include -DPostgreSQL_LIBRARY_RELEASE=/Applications/Postgres.app/Contents/Versions/15/lib



gdal_JPEG, JPEG image format
 * gdal_RAW, Raw formats:EOSAT FAST Format, FARSITE LCP and Vexcel MFF2 Image
 * gdal_GTIFF, GeoTIFF image format
 * gdal_MEM, Read/write data in Memory
 * gdal_VRT, Virtual GDAL Datasets
 * gdal_HFA, Erdas Imagine .img
 * gdal_SDTS, SDTS translator
 * gdal_NITF, National Imagery Transmission Format
 * gdal_GXF, GXF
 * gdal_AAIGRID, Arc/Info ASCII Grid Format.
 * gdal_CEOS, CEOS translator
 * gdal_SAR_CEOS, ASI CEOS translator
 * gdal_XPM, XPM image format
 * gdal_DTED, Military Elevation Data
 * gdal_JDEM, JDEM driver
 * gdal_ENVISAT, Envisat
 * gdal_ELAS, Earth Resources Laboratory Applications Software
 * gdal_FIT, FIT driver
 * gdal_L1B, NOAA Polar Orbiter Level 1b Data Set (AVHRR)
 * gdal_RS2, RS2 -- RadarSat 2 XML Product
 * gdal_ILWIS, Raster Map
 * gdal_RMF, RMF --- Raster Matrix Format
 * gdal_LEVELLER, Daylon Leveller heightfield
 * gdal_SGI, SGI Image driver
 * gdal_SRTMHGT, SRTM HGT File Read Support
 * gdal_IDRISI, Idrisi Raster Format
 * gdal_GSG, Implements the Golden Software Surfer 7 Binary Grid Format.
 * gdal_ERS, ERMapper .ERS
 * gdal_JAXAPALSAR, JAXA PALSAR Level 1.1 and Level 1.5 processed products support
 * gdal_DIMAP, SPOT Dimap Driver
 * gdal_GFF, Ground-based SAR Applitcations Testbed File Format driver
 * gdal_COSAR, COSAR -- TerraSAR-X Complex SAR Data Product
 * gdal_PDS, USGS Astrogeology ISIS Cube (Version 2)
 * gdal_ADRG, ADRG reader and ASRP/USRP Reader
 * gdal_COASP, DRDC Configurable Airborne SAR Processor (COASP) data reader
 * gdal_TSX, TerraSAR-X XML Product Support
 * gdal_TERRAGEN, Terragen&trade; Terrain File
 * gdal_BLX, Magellan BLX Topo File Format
 * gdal_MSGN, Meteosat Second Generation (MSG) Native Archive Format (.nat)
 * gdal_TIL, EarthWatch .TIL Driver
 * gdal_R, R Object Data Store
 * gdal_NORTHWOOD, NWT_GRD/NWT_GRC -- Northwood/Vertical Mapper File Format
 * gdal_SAGA, SAGA GIS Binary Driver
 * gdal_XYZ, ASCII Gridded XYZ
 * gdal_HEIF, HEIF
 * gdal_ESRIC, ESRI compact cache
 * gdal_HF2, HF2/HFZ heightfield raster
 * gdal_KMLSUPEROVERLAY
 * gdal_CTG, CTG driver
 * gdal_ZMAP, ZMAP
 * gdal_NGSGEOID, NOAA NGS Geoid Height Grids
 * gdal_IRIS, IRIS driver
 * gdal_MAP, OziExplorer .MAP
 * gdal_CALS, CALS type 1
 * gdal_SAFE, SAFE -- Sentinel-1 SAFE XML Product
 * gdal_SENTINEL2, Driver for Sentinel-2 Level-1B, Level-1C and Level-2A products.
 * gdal_PRF, PHOTOMOD Raster File
 * gdal_MRF, Meta raster format
 * gdal_WMTS, OGC Web Map Tile Service
 * gdal_GRIB, WMO General Regularly-distributed Information in Binary form
 * gdal_BMP, Microsoft Windows Device Independent Bitmap
 * gdal_TGA, TGA
 * gdal_STACTA, STACTA
 * gdal_BSB, Maptech/NOAA BSB Nautical Chart Format
 * gdal_AIGRID, Arc/Info Binary Grid Format
 * gdal_ARG, ARG: Azavea Raster Grid
 * gdal_USGSDEM, USGS ASCII DEM (and CDED)
 * gdal_AIRSAR, AirSAR Polarimetric Format
 * gdal_OZI, OZF2/OZFX3 raster
 * gdal_PCIDSK, PCI Geomatics Database File
 * gdal_SIGDEM, Scaled Integer Gridded DEM .sigdem Driver
 * gdal_RIK, RIK -- Swedish Grid Maps
 * gdal_STACIT, STACIT
 * gdal_PDF, Geospatial PDF
 * gdal_PNG, PNG image format
 * gdal_GIF, Graphics Interchange Format
 * gdal_WCS, OGC Web Coverage Service
 * gdal_HTTP, HTTP driver
 * gdal_NETCDF, NetCDF network Common Data Form
 * gdal_ZARR, ZARR
 * gdal_DAAS, Airbus DS Intelligence Data As A Service(DAAS)
 * gdal_EEDA, Earth Engine Data API
 * gdal_FITS, FITS Driver
 * gdal_HDF5, Hierarchical Data Format Release 5 (HDF5)
 * gdal_PLMOSAIC, PLMosaic (Planet Labs Mosaics API)
 * gdal_WMS, Web Map Services
 * gdal_OGCAPI, OGCAPI
 * gdal_WEBP, WebP
 * gdal_RASTERLITE, Rasterlite - Rasters in SQLite DB
 * gdal_MBTILES, MBTile
 * gdal_JP2OPENJPEG, JPEG2000 driver based on OpenJPEG library
 * gdal_EXR, EXR support via OpenEXR library
 * gdal_PCRASTER, PCRaster CSF 2.0 raster file driver
 * gdal_JPEGXL, JPEG-XL
 * ogr_MEM, Read/write driver for MEMORY virtual files
 * ogr_GEOJSON, GeoJSON/ESRIJSON/TopoJSON driver
 * ogr_TAB, MapInfo TAB and MIF/MID
 * ogr_SHAPE, ESRI shape-file
 * ogr_KML, KML
 * ogr_VRT, VRT - Virtual Format
 * ogr_AVC, AVC
 * ogr_GML, GML
 * ogr_CSV, CSV
 * ogr_DGN, DGN
 * ogr_GMT, GMT
 * ogr_NTF, NTF
 * ogr_S57, S57
 * ogr_TIGER, U.S. Census TIGER/Line
 * ogr_GEOCONCEPT, GEOCONCEPT
 * ogr_GEORSS, GEORSS
 * ogr_DXF, DXF
 * ogr_PGDUMP, PGDump
 * ogr_GPSBABEL, GPSBABEL
 * ogr_EDIGEO, EDIGEO
 * ogr_SXF, SXF
 * ogr_OPENFILEGDB, OPENFILEGDB
 * ogr_WASP, WAsP .map format
 * ogr_SELAFIN, OSELAFIN
 * ogr_JML, JML
 * ogr_VDV, VDV-451/VDV-452/INTREST Data Format
 * ogr_FLATGEOBUF, FlatGeobuf
 * ogr_MAPML, MapML
 * ogr_JSONFG, JSONFG
 * ogr_SDTS, SDTS
 * ogr_GPX, GPX - GPS Exchange Format
 * ogr_GMLAS, GMLAS
 * ogr_SVG, Scalable Vector Graphics
 * ogr_CSW, CSW
 * ogr_LIBKML, LibKML
 * ogr_NAS, NAS/ALKIS
 * ogr_PLSCENES, PLSCENES
 * ogr_WFS, OGC WFS service
 * ogr_NGW, NextGIS Web
 * ogr_ELASTIC, ElasticSearch
 * ogr_IDRISI, IDRISI
 * ogr_PDS, Planetary Data Systems TABLE
 * ogr_SQLITE, SQLite3 / Spatialite RDBMS
 * ogr_GPKG, GeoPackage
 * ogr_OSM, OpenStreetMap XML and PBF
 * ogr_VFK, Czech Cadastral Exchange Data Format
 * ogr_MVT, MVT
 * ogr_PMTILES, PMTiles
 * ogr_AMIGOCLOUD, AMIGOCLOUD
 * ogr_CARTO, CARTO
 * ogr_ILI, ILI
 * ogr_MSSQLSPATIAL, MSSQLSPATIAL
 * ogr_ODBC, ODBC
 * ogr_PGEO, PGEO
 * ogr_XLSX, Microsoft Office Excel(xlsx)
 * ogr_XLS, Microsoft Office Excel(xls)
 * ogr_CAD, OpenCAD
 * ogr_PARQUET, Parquet
 * ogr_ARROW, Arrow
 * ogr_GTFS, GTFS
 * ogr_ODS, ODS
 * ogr_LVBAG, LVBAG





 * ODBC
   Enable DB support through ODBC
 * Iconv
   Character set recoding (used in GDAL portability library)
 * LibXml2
   Read and write XML formats
 * XercesC
   Read and write XML formats (needed for GMLAS and ILI drivers)
 * ZSTD
   ZSTD compression library
 * GIF
   GIF compression library (external)
 * JSONC
   json-c library (external)
 * PCRE2
   Enable PCRE2 support for sqlite3
 * SPATIALITE (required version >= 4.1.2)
   Enable spatialite support for sqlite3
 * LibKML
   Use LIBKML library
 * HDF5
   Enable HDF5
 * WebP
   WebP compression
 * FreeXL
   Enable XLS driver
 * CFITSIO
   C FITS I/O library
 * NetCDF
   Enable netCDF driver
 * OpenCL
   Enable OpenCL (may be used for warping)
 * LibLZMA
   LZMA compression
 * LZ4
   LZ4 compression
 * LIBAEC
   Adaptive Entropy Coding implementing Golomb-Rice algorithm (used by GRIB)
 * JXL
   JPEG-XL compression
 * JXL_THREADS
   JPEG-XL threading
 * OpenEXR
   OpenEXR >=2.2
 * HEIF
   HEIF >= 1.1
 * OpenJPEG
 * Poppler, A PDF rendering library, <http://poppler.freedesktop.org>
   Enable PDF driver with Poppler (read side)
 * Snappy
 * OpenSSL
   Use OpenSSL library
 * ZLIB
   zlib (external)
 * lz4
 * zstd
 * re2
 * AWSSDK
 * Arrow
   Apache Arrow C++ library
 * Parquet
   Apache Parquet C++ library
 * ArrowDataset
   Apache ArrowDataset C++ library
 * Java
 * BISON
