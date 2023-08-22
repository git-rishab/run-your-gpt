import {
  Paper,
  createStyles,
  TextInput,
  PasswordInput,
  Button,
  Title,
  Text,
  Anchor,
  rem,
  Loader,
} from "@mantine/core";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { notification, url } from "../notification";

const useStyles = createStyles((theme) => ({
  wrapper: {
    minHeight: rem(900),
    backgroundSize: "cover",
    backgroundImage:
      "url(https://images.unsplash.com/photo-1484242857719-4b9144542727?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1280&q=80)",
  },

  form: {
    borderRight: `${rem(1)} solid ${
      theme.colorScheme === "dark" ? theme.colors.dark[7] : theme.colors.gray[3]
    }`,
    minHeight: rem(900),
    maxWidth: rem(450),
    paddingTop: rem(80),

    [theme.fn.smallerThan("sm")]: {
      maxWidth: "100%",
    },
  },

  title: {
    color: theme.colorScheme === "dark" ? theme.white : theme.black,
    fontFamily: `Greycliff CF, ${theme.fontFamily}`,
  },
}));

export default function Register() {
  const { classes } = useStyles();
  const redirect = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loader, setloader] = useState(false)
  const handleRegister = async() => {
    setloader(true)
    try {
        const req = await fetch(`${url}/user/register`,{
            method:"POST",
            headers:{
                "content-type":"application/json"
            },
            body:JSON.stringify({name,email,password})
        })
        const res = await req.json();
    
        if(res.ok){
            notification('Register Successfull', 'Login Now', 'white','#66BB6A');
            redirect('/login')
        } else {
            notification('Oops!', res.message, 'white', '#F44336')
        }
        
    } catch (error) {
        console.log(error);
        
    }
    setloader(false);
  };
  return (
    <div className={classes.wrapper}>
      <Paper className={classes.form} radius={0} p={30}>
        <Title order={2} className={classes.title} ta="center" mt="md" mb={50}>
          Welcome to Chat Application!
        </Title>
        <TextInput
          label="Name"
          placeholder="John"
          size="md"
          onChange={(e) => setName(e.target.value)}
        />
        <TextInput
          label="Email address"
          placeholder="hello@gmail.com"
          mt="md"
          size="md"
          onChange={(e) => setEmail(e.target.value)}
        />
        <PasswordInput
          label="Password"
          placeholder="Your password"
          mt="md"
          size="md"
          onChange={(e) => setPassword(e.target.value)}
        />
        <Button fullWidth mt="xl" size="md" onClick={handleRegister}>
          {loader ? <Loader size='sm' color="white"/> : 'Register'}
        </Button>

        <Text ta="center" mt="md">
          Already Registered?{" "}
          <Anchor<"a">
            href="#"
            weight={700}
            onClick={(event) => {
              event.preventDefault();
              redirect("/login");
            }}
          >
            Login
          </Anchor>
        </Text>
      </Paper>
    </div>
  );
}
