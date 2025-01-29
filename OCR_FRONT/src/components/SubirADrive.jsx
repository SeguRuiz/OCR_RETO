import { useState } from "react";
import { postDrive } from "../utils/requests";
import {
  Button,
  CircularProgress,
  Alert,
  Backdrop,
  Typography,
} from "@mui/material";
import AddToDriveIcon from "@mui/icons-material/AddToDrive";
import CheckIcon from "@mui/icons-material/Check";


const SubirADrive = ({ paginas = [], setContenidos, setDisabled }) => {
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const subirAdrive = async () => {
    setDisabled(true)
    setLoading(true)
    const [status, datos] = await postDrive(
      "http://localhost:8000/api/subir-a-drive/",
      { paginas: paginas }
    );
    if (status == 200) {
      setContenidos([]);
      setOpen(true);
    }else{
        alert('Ocurrio un error al subir los archivos')
    }
    setLoading(false);
    setDisabled(false)
  };
  return (
    <>
      <Button
        onClick={subirAdrive}
        variant="contained"
        startIcon={<AddToDriveIcon />}
        disabled={loading || paginas.length == 0}
      >
        {loading ? "Subiendo..." : "Añadir a drive"}
        {loading && (
          <CircularProgress
            sx={{
              position: "absolute",
            }}
            size={20}
          />
        )}
      </Button>
      <Backdrop
        open={open}
        onClick={() => {
          setOpen(false);
        }}
      >
        <Alert icon={<CheckIcon fontSize="inherit" />} severity="success">
          Loa archivos se subieron correctamente
        </Alert>
      </Backdrop>
    </>
  );
};

export default SubirADrive;
