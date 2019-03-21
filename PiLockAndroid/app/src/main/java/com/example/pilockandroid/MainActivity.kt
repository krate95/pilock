package com.example.pilockandroid

import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.Toast
import com.github.kittinunf.fuel.Fuel
import com.github.kittinunf.fuel.core.extensions.jsonBody

class MainActivity : AppCompatActivity() {



    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        /*val openButton = findViewById<Button>(R.id.openButton)
        openButton.setOnClickListener {
            Toast.makeText(this@MainActivity, "Abrir", Toast.LENGTH_SHORT).show()
            openRequest()
        }*/
        Fuel.post("http://krate.ddns.net:5000/open")
            .jsonBody("{ \"text\":\"Hola desde mi app Android\"}")
            .also { println(it) }
            .response { result -> }
    }

    private fun openRequest() {
        Fuel.post("http://krate.ddns.net:5000/open")
            .jsonBody("{ \"text\":\"Hola desde mi app Android\"}")
            .also { println(it) }
            .response { result -> }
    }


}
