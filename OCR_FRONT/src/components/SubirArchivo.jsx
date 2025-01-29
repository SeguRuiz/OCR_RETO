import { useRef, useState } from "react";
import { post } from "../utils/requests";
import SubirADrive from "./SubirADrive";

import { Button, CircularProgress } from "@mui/material";

import AttachFileIcon from "@mui/icons-material/AttachFile";

const textoExtraidoMock = [
  {
    fields: {
      solicitado_por: {
        numero: "",
        nombre: "Luis",
        correo: "ruiz96199@gmail.com",
        telefono: "84858324",
      },
      entregar_a: {
        correo: "ruiz96199@gmail.com",
        nombre: "Luisa",
        telefono: "78903452",
        direccion:
          "mdiqodjieujdiuejdiuemdiwemdiedijeewmociewmciwcjiowimcinweiucwiecinweciwuecuwecmw",
        notas:
          "ocjwejdjewoifjoiemdeofkmfkmwiorfmrimfolro k lwfomoiedmoef  fenfoefoefefff",
      },
    },
  },
];

const SubirArchivo = ({ setContenidos, contenidos = [] }) => {
  const inputRef = useRef(null);

  const [loading, setLoading] = useState(false);
  const [disabled, setDisabled] = useState(false);

  const eliminarPalabra = (texto = "", palabra = "") => {
    let array = texto.split("\n");

    return array.filter((x) => x != palabra).join(" ");
  };

  const serializarDatos = (datos = {}) => {
    const datosCopy = { ...datos };
    datosCopy.data.forEach((e) => {
      e.fields.solicitado_por.nombre = eliminarPalabra(
        e.fields.solicitado_por.nombre,
        "Teléfono"
      );

      e.fields.entregar_a.nombre = eliminarPalabra(
        e.fields.entregar_a.nombre,
        "Teléfono"
      );
    });

    return datosCopy;
  };

  const procesarArchivo = async (archivo) => {
    setLoading(true);
    const formData = new FormData();
    formData.append("file", archivo);
    const [status, datos] = await post(
      "http://localhost:8000/api/procesar-archivo-paginacion/",
      formData
    );

    if (status == 200) {
      setContenidos(serializarDatos(datos).data);
    }

    setLoading(false);

    inputRef.current.value = null;
  };

  const manejarCambioDeValor = (o) => {
    const archivo = o.target.files[0];
    if (archivo) {
      procesarArchivo(archivo);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        gap: "20px",
      }}
    >
      <input
        type="file"
        onChange={manejarCambioDeValor}
        ref={inputRef}
        style={{
          display: "none",
        }}
      />
      <Button
        startIcon={
          <>
            <AttachFileIcon />
          </>
        }
        fullWidth={false}
        disabled={loading || disabled}
        onClick={() => {
          inputRef.current && inputRef.current.click();
        }}
        variant="contained"
      >
        {loading ? "Escaneando..." : "Adjuntar archivos"}
        {loading && (
          <CircularProgress
            sx={{
              position: "absolute",
            }}
            size={20}
          />
        )}
      </Button>
      {
        <SubirADrive
          paginas={contenidos}
          setContenidos={setContenidos}
          setDisabled={setDisabled}
        />
      }
    </div>
  );
};

export default SubirArchivo;
