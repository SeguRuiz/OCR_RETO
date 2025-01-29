import { Card, CardHeader, Stack } from "@mui/material";
import ArticleIcon from "@mui/icons-material/Article";

const ArhcivosPreview = ({ archivos = [] }) => {
  return (
    <Stack spacing={1}>
      {archivos.map((x, i) => (
        <Card key={i} sx={{}}>
          <CardHeader
            title={`N° ${x.fields.solicitado_por.numero}`}
            avatar={<ArticleIcon />}
          />
        </Card>
      ))}
    </Stack>
  );
};

export default ArhcivosPreview;
