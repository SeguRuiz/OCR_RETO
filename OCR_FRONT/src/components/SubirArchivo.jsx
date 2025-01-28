import { useRef } from "react";
import { post } from "../utils/requests";

const SubirArchivo = () => {
  const inputRef = useRef(null);

  const procesarArchivo = async (archivo) => {
    const formData = new FormData();
    formData.append("archivo", archivo);
    const [status, datos] = await post(
      "http://localhost:8000/api/procesar-archivo/",
      formData
    );

    console.log(status, datos);

    inputRef.current.value = null;
  };

  const manejarCambioDeValor = (o) => {
    const archivo = o.target.files[0];
    if (archivo) {
      procesarArchivo(archivo);
    }
  };
  return (
    <>
      <input
        type="file"
        onChange={manejarCambioDeValor}
        ref={inputRef}
        style={{
          display: "none",
        }}
      />
      <button
        onClick={() => {
          inputRef.current && inputRef.current.click();
        }}
      >
        Selecciona el archivo
      </button>
    </>
  );
};

export default SubirArchivo;
