import { useState } from "react";
import { postDrive } from "../utils/requests";

const SubirADrive = ({ datos = {} }) => {
  const [loading, setLoading] = useState(false);
  const subirAdrive = async () => {
    setLoading(true);
    const [status, datos] = await postDrive(
      "http://localhost:8000/api/subir-a-drive/",
      {}
    );
    console.log(status, datos);

    setLoading(false);
  };
  return (
    <button onClick={subirAdrive}>
      {loading ? "Subiendo...." : "Subir a drive"}
    </button>
  );
};

export default SubirADrive;
