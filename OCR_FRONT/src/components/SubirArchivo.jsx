import { useRef, useState } from "react";
import { post } from "../utils/requests";
import SubirADrive from "./SubirADrive";

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

const SubirArchivo = () => {
  const inputRef = useRef(null);
  const [textoExtraido, setTextoExtraido] = useState([]);
  const [loading, setLoading] = useState(false);

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
      "http://localhost:8000/api/procesar-archivo-paga-paginacion-opencv/",
      formData
    );

    if (status == 200) {
      console.log(datos);
      
      setTextoExtraido(serializarDatos(datos).data);
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
    <>
      <div
        style={{
          width: "90vh",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          gap: "30px",
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
        <button
          onClick={() => {
            inputRef.current && inputRef.current.click();
          }}
        >
          {loading ? "Procesando..." : "Selecciona el archivo"}
        </button>
        {textoExtraido.length > 0 && <SubirADrive paginas={textoExtraido} />}
        {textoExtraido.map((x, i) => (
          <div key={i}>
            <h2>
              Pagina: {i + 1} N°{x.fields.solicitado_por.numero}
            </h2>
            <h2>Solicidato por:</h2>
            <p> Nombre: {x.fields.solicitado_por.nombre}</p>
            <p>Telefono: {x.fields.solicitado_por.telefono}</p>
            <p>Correo: {x.fields.solicitado_por.correo}</p>
            <br />
            <h2>Entregar a:</h2>
            <p>Nombre: {x.fields.entregar_a.nombre}</p>
            <p>Telefono: {x.fields.entregar_a.telefono}</p>
            <p>Direccion: {x.fields.entregar_a.direccion}</p>
            <p>Notas: {x.fields.entregar_a.notas}</p>
            <hr />
          </div>
        ))}
      </div>
    </>
  );
};

export default SubirArchivo;
