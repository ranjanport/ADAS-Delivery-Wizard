import sys, os
from PyQt5.QtWidgets import  QApplication, QMainWindow, QFileDialog, QMessageBox
from adas import Ui_ADAS_UTILITY
from osgeo import ogr
import os.path
import configparser

sys.path.insert(0, os.path.join(os.path.dirname(sys.path[0])))

SERVER_CONFIG_PATH = sys.path[0]
OVERIDE_SERVER_PATH = False

if SERVER_CONFIG_PATH and OVERIDE_SERVER_PATH:
    DATABASE = "adas"
    USER = "postgres"
    SCHEMA = "aman"
    PASSWORD = "postgres"
    HOST = "localhost"  # Change this to your database host if needed
    PORT = 5432  # Change this to your database port if needed
    SRS = "EPSG:4326"
else:
    configs = configparser.ConfigParser()
    configs.read(os.path.join(SERVER_CONFIG_PATH, 'adas_delivery_confs.ini'))
    dbConfigs = configs['initconfig']
    
    DATABASE = dbConfigs['DATABASE']
    USER = dbConfigs['USER']
    SCHEMA = dbConfigs['SCHEMA']
    PASSWORD = dbConfigs['PASSWORD']
    HOST = dbConfigs['HOST']  # Change this to your database host if needed
    PORT = dbConfigs['PORT']  # Change this to your database port if needed
    SRS = dbConfigs['SRS']
    
# Static Functions
def show_critical_messagebox(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    # setting message for Message Box
    msg.setText(message)
    # setting Message box window title
    msg.setWindowTitle("Authorization Alert!")
    # declaring buttons on Message Box
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    # start the app
    retval = msg.exec_()

def show_warning_messagebox(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    # setting message for Message Box
    msg.setText(message)
    # setting Message box window title
    msg.setWindowTitle('Warning!')
    # declaring buttons on Message Box
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    # start the app
    retval = msg.exec_()

def show_ifo_messagebox(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    # setting message for Message Box
    msg.setText(message)
    # setting Message box window title
    msg.setWindowTitle("Information!")
    # declaring buttons on Message Box
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    # start the app
    retval = msg.exec_()

class ADASUtilityApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_ADAS_UTILITY()
        self.ui.setupUi(self)

        self.ui.pb1.clicked.connect(self.select_ROAD_LAYER)
        self.ui.pb2.clicked.connect(self.select_ELEVATION_LAYER)
        self.ui.pb3.clicked.connect(self.select_JUNCTION_LAYER)
        self.ui.pb4.clicked.connect(self.select_OUTPUT_PATH)
        self.ui.pbRun.clicked.connect(self.run_process)
        self.ui.pbCancel.clicked.connect(self.close)

    def select_ROAD_LAYER(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Road Network Layer", "", "Tab Files (*.tab);;Shape Files (*.shp)")
        if file_path:
            self.ui.lineEdit.setText(file_path)

    def select_ELEVATION_LAYER(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Elevation Layer", "", "Tab Files (*.tab);;Shape Files (*.shp)")
        if file_path:
            self.ui.ln2.setText(file_path)

    def select_JUNCTION_LAYER(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Junction Layer", "", "Tab Files (*.tab);;Shape Files (*.shp)")
        if file_path:
            self.ui.ln3.setText(file_path)

    def select_OUTPUT_PATH(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Path")
        if directory:
            self.ui.ln4.setText(directory)
            
    def copy_layer_to_postgres(self, input_file, database_name, schema_name, user, password, host='localhost', port=5432, srs='EPSG:4326'):
        try:
            # Open the input file
            input_ds = ogr.Open(input_file)
            if input_ds is None:
                show_critical_messagebox(f"Could not open file: {input_file}")
                return
            
            input_layer = input_ds.GetLayer()
            
            # Extract table name from input file
            table_name = os.path.splitext(os.path.basename(input_file))[0]

            # Connect to the PostgreSQL database
            conn_str = f"PG:host={host} user={user} port={port} password={password} dbname={database_name}"
            conn = ogr.Open(conn_str)
            if conn is None:
                show_critical_messagebox(f"Could not connect to the database. Contact Support")
                return
            
            # Set the SRS
            target_srs = ogr.osr.SpatialReference()
            target_srs.SetFromUserInput(srs)

            # Get the PostgreSQL driver
            ogr_pg = ogr.GetDriverByName('PostgreSQL')
            if ogr_pg is None:
                show_warning_messagebox(f"PostgreSQL driver not available.")
                return
            
            # Create a new data source for PostgreSQL
            out_ds = ogr_pg.CreateDataSource(conn_str)
            if out_ds is None:
                show_warning_messagebox("Could not create data source in PostgreSQL.")
                return

            # Create a new layer in the PostgreSQL data source
            out_layer = out_ds.CreateLayer(table_name, srs=target_srs, geom_type=input_layer.GetGeomType(), options=[f'OVERWRITE=YES', f'SCHEMA={schema_name}'])
            if out_layer is None:
                show_critical_messagebox("Could not create layer in PostgreSQL data source.")
                return
            
            # Copy fields from input layer to output layer
            for i in range(input_layer.GetLayerDefn().GetFieldCount()):
                field_defn = input_layer.GetLayerDefn().GetFieldDefn(i)
                out_layer.CreateField(field_defn)
            
            counter = 0
            total_features = input_layer.GetFeatureCount()
            self.ui.progressBarLabel.setText(f"Uploading : {table_name}")
            # Copy features from input layer to output layer
            for feature in input_layer:
                out_layer.CreateFeature(feature)
                percentageDone = int(counter * 100 / total_features)
                counter+=1
                try:
                    self.ui.progressCounter.setText(f"{counter} / {total_features} : {percentageDone}%")
                    self.ui.progressBar.setValue(percentageDone)
                    QApplication.processEvents()
                except:
                    show_ifo_messagebox("Unable to Increment Value")
            # Clean up
            out_ds = None
            input_ds = None
            conn = None
            self.ui.progressCounter.setText(f"")
            QApplication.processEvents()
            self.ui.progressBarLabel.setText(f"Uploaded : {table_name}")
            QApplication.processEvents()
            self.ui.progressBarLabel.setText(f"Please Wait ...")
            QApplication.processEvents()
            return True
        except Exception as e:
            return False

    def save_layer_to_file(self, table_name, outFileType, extenstion,  output_path, database_name, schema_name, user, password, host='localhost', port=5432, srs='EPSG:4326'):
        
        self.ui.progressBarLabel.setText(f"Exporting : {table_name}")
        QApplication.processEvents()
        output_file = os.path.join(output_path, table_name+extenstion)
        # Connect to the PostgreSQL database
        conn_str = f"PG:host={host} user={user} port={port} password={password} dbname={database_name}"
        conn = ogr.Open(conn_str)
        if conn is None:
            print("Could not connect to the database.")
            return

        # Get the PostgreSQL driver
        ogr_pg = ogr.GetDriverByName('PostgreSQL')
        if ogr_pg is None:
            print("PostgreSQL driver not available.")
            return
        
        if outFileType == "ESRI":
        # Create a new data source for the output file
            out_ds = ogr.GetDriverByName('ESRI Shapefile').CreateDataSource(output_file)
        else:
            out_ds = ogr.GetDriverByName('MapInfo File').CreateDataSource(output_file)
        if out_ds is None:
            print("Could not create output data source.")
            return
        
        # Set the SRS
        target_srs = ogr.osr.SpatialReference()
        target_srs.SetFromUserInput(srs)

        # Create a new layer in the output data source
        out_layer = out_ds.CreateLayer(table_name, srs=target_srs, geom_type=ogr.wkbUnknown)
        if out_layer is None:
            print("Could not create output layer.")
            return

        # Connect to the input table in PostgreSQL
        input_layer = conn.GetLayerByName(f"{schema_name}.{table_name}")
        if input_layer is None:
            print("Input table not found in PostgreSQL.")
            return

        # Copy fields from input layer to output layer
        for i in range(input_layer.GetLayerDefn().GetFieldCount()):
            field_defn = input_layer.GetLayerDefn().GetFieldDefn(i)
            out_layer.CreateField(field_defn)

        # Copy features from input layer to output layer
        for feature in input_layer:
            out_layer.CreateFeature(feature)

        # Clean up
        out_ds = None
        conn = None
        
        return True

    def doQuery(self):
        pass
        
        
    def update_progress(self, value):
        # Update progress bar value
        self.ui.progressBar.setValue(value)
        QApplication.processEvents()
        
    def run_process(self):
        self.update_progress(0)
        ROAD_LAYER = self.ui.lineEdit.text()
        ELEVATION_LAYER = self.ui.ln2.text()
        JUNCTION_LAYER = self.ui.ln3.text()
        OUTPUT_PATH = self.ui.ln4.text()
    
        isReady = False
        if  ROAD_LAYER:
            if ELEVATION_LAYER:
                if JUNCTION_LAYER:
                    if OUTPUT_PATH:
                        if self.ui.rdMapinfo.isChecked():
                            OUT_FILE_TYPE = "MapInfo"
                            EXTENSION = '.tab'
                            isReady = True
                            overallProgress = 10
                            self.update_progress(overallProgress)
                        elif self.ui.rdEsri.isChecked():
                            outFileType = "ESRI"
                            extension = '.shp'
                            isReady = True
                            overallProgress = 10
                            self.update_progress(overallProgress)
                        else:
                            show_warning_messagebox("Please Select File Type!")
                    else:
                        show_warning_messagebox("Output Path Not Provided!")
                else:
                    show_warning_messagebox("Junctiion Layer Required!")
            else:
                show_warning_messagebox("Elevation Layer Required!")
        else:
            show_warning_messagebox("Road Network Required!")
        
        if isReady:
            if self.copy_layer_to_postgres(ROAD_LAYER, DATABASE, SCHEMA, USER, PASSWORD, HOST, PORT, SRS):
                overallProgress+=20
                self.update_progress(overallProgress)
                self.ui.progressBar.setMaximum(100)
                QApplication.processEvents()
                if self.copy_layer_to_postgres(ELEVATION_LAYER, DATABASE, SCHEMA, USER, PASSWORD, HOST, PORT, SRS):
                    overallProgress+=20
                    self.update_progress(overallProgress)
                    self.ui.progressBar.setMaximum(100)
                    QApplication.processEvents()
                    if self.copy_layer_to_postgres(JUNCTION_LAYER, DATABASE, SCHEMA, USER, PASSWORD, HOST, PORT, SRS):
                        overallProgress+=20
                        self.update_progress(overallProgress)
                        self.ui.progressBar.setMaximum(100)
                        QApplication.processEvents()
                        try:
                            if self.doQuery():
                                overallProgress+=10
                                self.update_progress(overallProgress)
                                self.ui.progressBar.setMaximum(100)
                                QApplication.processEvents()
                                pass  # ADD ALGO
                            
                                table_names = ["dfs", "fds", "fdse"]
                                try:
                                    for table_name in table_names:
                                        if self.save_layer_to_file(table_name, OUT_FILE_TYPE, EXTENSION, OUTPUT_PATH, DATABASE, SCHEMA, USER, PASSWORD, HOST, PORT, SRS):
                                            overallProgress+=10
                                            self.update_progress(overallProgress)
                                            self.ui.progressBar.setMaximum(100)
                                            QApplication.processEvents()
                                            self.ui.progressBarLabel.setText(f"Exported : {table_name}")
                                            QApplication.processEvents()
                                    show_ifo_messagebox(f"Process Completed : Please Refer Path : {OUTPUT_PATH}")
                                except Exception as e:
                                    show_warning_messagebox("Something Went Wrong While Exporting Layers -> Contact Support")
                        except Exception as e:
                            show_critical_messagebox("Something Went Wrong While Processing ADAS Algorithm -> Contact Support")
                    else:
                        show_critical_messagebox("Unable to Upload JUNCTION Layer")
                else:
                    show_critical_messagebox("Unable to Upload ELEVATION Layer")
            else:
                show_critical_messagebox("Unable to Upload ROAD Layer")
           
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ADASUtilityApp()
    main_window.show()
    app.processEvents()
    sys.exit(app.exec_())
