import { useRef } from "react";
import { subirArhivo } from "../utils/requests";

const SubirArchivo = () => {
  const inputRef = useRef(null);

  const manejarCambioDeValor = (o) => {
    const archivo = o.target.files[0];
    if (archivo) {
      console.log(archivo);
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
          // inputRef.current && inputRef.current.click();
          subirArhivo();
        }}
      >
        Selecciona el archivo
      </button>
    </>
  );
};

export default SubirArchivo;
